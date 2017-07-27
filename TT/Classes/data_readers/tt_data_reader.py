# -*- coding: utf-8 -*-
from solutions.tt_solution.resource import Resource
from solutions.tt_solution.types import ResourceType

from solutions.tt_solution.tt_solution import TtSolution
from .data_reader import DataReader
from bs4 import BeautifulSoup


class TtDataReader(DataReader):
    def read(self, source_filename):
        with open(source_filename, 'r') as f:
            soup = BeautifulSoup(f.read(), "lxml")

        # get the rooms in the university
        rooms = {}
        
        for room in soup.rooms.findChildren(recursive=False):
            properties = {'capacity': int(room['capacity'])}
            location = room['location'].split(",")
            properties['location'] = {'x': location[0], 'y': location[1]}
            
            if room.has_attr('ignoreTooFar'):
                properties['ignoreTooFar'] = bool(room['ignoreTooFar'])
            else:
                properties['ignoreTooFar'] = False
                
            if room.has_attr('discouraged'):
                properties['discouraged'] = bool(room['discouraged'])
            else:
                properties['discouraged'] = False
                
            if room.has_attr('constraint'):
                properties['constraint'] = bool(room['constraint'])
            else:
                properties['constraint'] = True
            
            # TODO: check if sharing tag is necessary
            
            room_entity = Resource(int(room['id']), ResourceType.Room, properties)
            rooms[int(room['id'])] = room_entity
            
        # get the classes of the university
        university_classes = {}
        all_instructors = set()
        
        for university_class in soup.classes.findChildren(recursive=False):
            properties = {'constraints': {}}
        
            if university_class.has_attr('offering'):
                properties['offering'] = int(university_class['offering'])
                
            if university_class.has_attr('config'):
                properties['config'] = int(university_class['config'])

            if university_class.has_attr('parent'):
                properties['parent'] = int(university_class['parent'])

            if university_class.has_attr('scheduler'):
                properties['scheduler'] = int(university_class['scheduler'])
                
            if university_class.has_attr('department'):
                properties['department'] = int(university_class['department'])
                
            if university_class.has_attr('committed'):
                properties['committed'] = university_class['committed']
            else:
                properties['committed'] = False

            if university_class.has_attr('classLimit'):
                properties['classLimit'] = int(university_class['classLimit'])
                
            if university_class.has_attr('minClassLimit'):
                properties['minClassLimit'] = int(university_class['minClassLimit'])
                
            if university_class.has_attr('maxClassLimit'):
                properties['maxClassLimit'] = int(university_class['maxClassLimit'])
                
            if university_class.has_attr('roomToLimitRatio'):
                properties['roomToLimitRatio'] = float(university_class['roomToLimitRatio'])
            else:
                properties['roomToLimitRatio'] = 1.0
                
            if university_class.has_attr('nrRooms'):
                properties['nrRooms'] = int(university_class['nrRooms'])
            else:
                properties['nrRooms'] = 1

            # class may have assigned instructors
            instructors = []
            for instructor in university_class.findAll('instructor'):
                instance = {'id': instructor['id']}
                if instructor.has_attr('solution'):
                    instance['solution'] = instructor['solution']
                instructors.append(instance)
                # TODO: look for a way to fix this
                all_instructors.add(instance['id'])
                
            properties['instructors'] = instructors

            # class may have desired rooms
            preferred_rooms = []
            for room in university_class.findAll('room'):
                instance = {'id': int(room['id'])}
                if room.has_attr('solution'):
                    instance['solution'] = room['solution']
                if room.has_attr('pref'):
                    instance['pref'] = float(room['pref'])
                preferred_rooms.append(instance)
   
            properties['rooms'] = preferred_rooms

            # classes have desired time slots
            time_slots = []
            for time_slot in university_class.findAll('time'):
                instance = {}
                if time_slot.has_attr('days'):
                    instance['days'] = time_slot['days']
                if time_slot.has_attr('start'):
                    instance['start'] = int(time_slot['start'])
                if time_slot.has_attr('length'):
                    instance['length'] = int(time_slot['length'])
                if time_slot.has_attr('pref'):
                    instance['pref'] = float(time_slot['pref'])
                if time_slot.has_attr('solution'):
                    instance['solution'] = time_slot['solution']
                    
                time_slots.append(instance)
                
            properties['time_slots'] = time_slots

            class_entity = Resource(int(university_class['id']), ResourceType.Class, properties)
            university_classes[int(university_class['id'])] = class_entity
            
        # get the constraints defined for different classes
        
        constraints = []
        for gConstraint in soup.findAll('constraint'):
            properties = {'type': gConstraint['type']}
            
            if gConstraint.has_attr('pref'):
                properties['pref'] = gConstraint['pref']
            if gConstraint.has_attr('courseLimit'):
                properties['courseLimit'] = float(gConstraint['courseLimit'])
            if gConstraint.has_attr('delta'):
                properties['delta'] = float(gConstraint['delta'])
            else:
                properties['delta'] = 0.0

            # add the classes involved in this contraint group
            classes = []
            for c in gConstraint.findAll('class'):
                classes.append(int(c['id']))
                
            properties['classes'] = classes
            
            constraint_entity = Resource(int(gConstraint['id']), ResourceType.ConstraintGroup, properties)
            constraints.append(constraint_entity)
            
        # get the enrolled students
        students = []
        for student in soup.students.findChildren(recursive=False):
            properties = {'offering': [],
                          'class': []}
            
            for offering in student.findAll('offering'):
                properties['offering'].append(int(offering['id']))
                
            for u_class in student.findAll('class'):
                properties['class'].append(int(u_class['id']))
                
            student_entity = Resource(int(student['id']), ResourceType.Student, properties)
            students.append(student_entity)
            
        print("Students: {0}".format(len(students)))
        print("Classes: {0}".format(len(university_classes)))
        print("Rooms: {0}".format(len(rooms)))
        print("Instuctors: {0}".format(len(all_instructors)))
        
        result = {"classes": university_classes,
                  "students": students,
                  "rooms": rooms,
                  "instructors": all_instructors,
                  "constraints": constraints}
        
        # classes will map to their constraints to ease access
        for k, uc in university_classes.items():
            for constraint in constraints:
                if uc.uid in constraint.properties['classes']:
                    if constraint.properties['type'] not in uc.properties['constraints']:
                        uc.properties['constraints'][constraint.properties['type']] = []
                    for uid in constraint.properties['classes']:
                        uc.properties['constraints'][constraint.properties['type']].append(uid)
                        
        enrollments = {}
        for student in students:
            for c_id in student.properties['class']:
                if c_id in enrollments:
                    enrollments[c_id].append(student.uid)
                else:
                    enrollments[c_id] = [student.uid]
                    
        result['enrollments'] = enrollments
        return TtSolution(result)
