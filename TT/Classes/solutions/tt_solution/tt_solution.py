# -*- coding: utf-8 -*-
import sys
from functools import cmp_to_key

from TT.Classes.solutions.solution import Solution
from TT.Classes.solutions.tt_solution.Event import Event
from TT.Classes.solutions.tt_solution.restrictions.same_room_and_time import SameRoomAndTime
from TT.Classes.solutions.tt_solution.restrictions.same_students import SameStudents
from TT.Classes.solutions.tt_solution.types import Day


def compare(item1, item2):
    diff_num_rooms = len(item1.properties['rooms']) - len(item2.properties['rooms'])
    
    if diff_num_rooms != 0:
        return diff_num_rooms
    
    diff_times = len(item1.properties['time_slots']) - len(item2.properties['time_slots'])
    
    return diff_times


class TtSolution(Solution):
    def __init__(self, state):
        super(TtSolution, self).__init__()
        self.state = state
        self.solution_space = self._find_initial_solution()
        self.isBacktracking = True
        self.stack = []
        self.candidates = self._get_candidates()
        self.preference = 0
        
    def _get_candidates(self):
        result = []

        for k, sol in self.state['classes'].items():
            if sol.properties['committed'] == "false" and len(sol.properties['rooms']) == 0 and \
                    len(sol.properties['time_slots']) == 0:
                result.append(k)
                
        for k, sol in self.state['classes'].items():
            if sol.properties['committed'] == "false" and len(sol.properties['rooms']) == 0 and \
                    len(sol.properties['time_slots']) > 0:
                result.append(k)
                
        for k, sol in self.state['classes'].items():
            if sol.properties['committed'] == "false" and len(sol.properties['rooms']) > 0 and \
                    len(sol.properties['time_slots']) == 0:
                result.append(k)
                
        holder = []
        for _, sol in self.state['classes'].items():
            if sol.properties['committed'] == "false" and len(sol.properties['rooms']) > 0 and \
                    len(sol.properties['time_slots']) > 0:
                holder.append(sol)
                
        holder = sorted(holder, key=cmp_to_key(compare), reverse=True)
                
        for elem in holder:
            result.append(elem.uid)
            
        for k, sol in self.state['classes'].items():
            if sol.properties['committed'] == "true" and len(sol.properties['rooms']) == 0:
                result.append(k)
                
        return result
        
    def _get_day(self, index):
        if index == 0:
            day = Day.Monday
        elif index == 1:
            day = Day.Tuesday
        elif index == 2:
            day = Day.Wednesday
        elif index == 3:
            day = Day.Thursday
        else:
            day = Day.Friday
            
        return day
    
    def find_slot(self, ci):
        if len(ci.properties['rooms']) > 0 and len(ci.properties['time_slots']) > 0:
            if ci.properties['time_slot_index'] < len(ci.properties['time_slots']):
                time_slot = ci.properties['time_slots'][ci.properties['time_slot_index']]
                days = []
                for index, day in enumerate(time_slot['days']):
                    if day == '1':
                        days.append(self._get_day(index))
                    
                room = ci.properties['rooms'][ci.properties['room_index']]['id']
                room = self.state['rooms'][room]
            
                return days, room, time_slot['start'], time_slot['length']
            
        # no preference slot found, look in other rooms
        if len(ci.properties['time_slots']) > 0:
            if ci.properties['time_slot_index'] < len(ci.properties['time_slots']):
                time_slot = ci.properties['time_slots'][ci.properties['time_slot_index']]
                days = []
                for index, day in enumerate(time_slot['days']):
                    if day == '1':
                        days.append(self._get_day(index))
                        
                index = ci.properties['room_search']
                
                room_key = list(self.state['rooms'].keys())[index]
                room = self.state['rooms'][room_key]

                return days, room, time_slot['start'], time_slot['length']

        # no slot found,
        return [], None, None, None
    
    def is_feasible(self, sol, days, room, time_start, time_length):
        for day in days:
            event = Event(day, time_start, time_length, room.uid, sol.uid)
            if SameRoomAndTime().is_violated(self, event) or SameStudents().is_violated(self, event):
                return False
            
        return True
        
    def permute(self, heuristic):
        # do the backtracking and return a new solution
        if self.isBacktracking:
            if len(self.candidates) > 0:
                sol = self.state['classes'][self.candidates[-1]]
                
                days, room, start, length = self.find_slot(sol)
                
                if room is not None:
                    if self.is_feasible(sol, days, room, start, length):
                        self.solution_space[sol.uid] = []
                        
                        for day in days:
                            self.solution_space[sol.uid].append(Event(day, start, length, room.uid, sol.uid))

                            rooms = self.state['rooms']
    
                            room_index = 0
                            for i, r in rooms.items():
                                if r.uid == room:
                                    break
                                    
                                room_index += 1
                            print("######### secceded ({0}) #########".format(len(self.candidates)))
                            print("id: {0}, com: {1}, rid: {2}, days: {3}, {4}:{5}".format(
                                sol.uid, sol.properties['committed'], room.uid, days, start, length))

                        self.stack.append(self.candidates.pop())
                        self.preference -= 1
                        return self

                    print("######### failed ({0}) #########".format(len(self.candidates)))
                    print("id: {0}, com: {1}, rid: {2}, days: {3}, {4}:{5}".format(
                        sol.uid, sol.properties['committed'], room.uid, days, start, length))

                print("######### No slot ({0}) #########".format(len(self.candidates)))
                # do reset and backtracking if necessary
                if 'room_index' in sol.properties:
                    if sol.properties['room_index'] < len(sol.properties['rooms']) - 1:
                        sol.properties['room_index'] += 1
                        return self

                if 'time_slot_index' in sol.properties and sol.properties['phase1']:
                    if sol.properties['time_slot_index'] < len(sol.properties['time_slots']) - 1:
                        if len(sol.properties['rooms']) > 0:
                            sol.properties['room_index'] = 0
                            sol.properties['time_slot_index'] += 1
                            return self
                        else:
                            if sol.properties['room_search'] < len(self.state['rooms']) - 1:
                                sol.properties['room_search'] += 1
                            else:
                                sol.properties['time_slot_index'] += 1
                                sol.properties['room_search'] = 0
                            
                            return self
                        
                # the class has to look in other classrooms
                if 'time_slot_index' in sol.properties:
                    if sol.properties['time_slot_index'] >= len(sol.properties['time_slots']) and \
                                    len(sol.properties['rooms']) > 0:
                        if sol.properties['phase1']:
                            sol.properties['time_slot_index'] = 0
                            sol.properties['phase1'] = False

                if 'time_slot_index' in sol.properties:
                    if sol.properties['time_slot_index'] < len(sol.properties['time_slots']) - 1:

                        if sol.properties['room_search'] < len(self.state['rooms']) - 1:
                            sol.properties['room_search'] += 1
                        else:
                            sol.properties['time_slot_index'] += 1
                            sol.properties['room_search'] = 0

                        return self
                
                # no solution found, start backtracking
                sol.properties['time_slot_index'] = 0
                # TODO: check likely cause of bug
                # sol.properties['room_search'] = 0
                sol.properties['time_search'] = 0
                sol.properties['room_index'] = 0
                sol.properties['room_search'] = 0
                sol.properties['phase1'] = True
               
                if len(self.stack) > 0:
                    sol_key = self.stack.pop()
                    sol = self.state['classes'][sol_key]
                    self.candidates.append(sol_key)

                    if 'room_index' in sol.properties:
                        if sol.properties['room_index'] < len(sol.properties['rooms']) - 1:
                            sol.properties['room_index'] += 1
                            return self

                    if 'time_slot_index' in sol.properties:
                        if sol.properties['time_slot_index'] < len(sol.properties['time_slots']) - 1:
                            if len(sol.properties['rooms']) > 0:
                                sol.properties['room_index'] = 0
                                sol.properties['time_slot_index'] += 1
                                return self
                            else:
                                if sol.properties['room_search'] < len(self.state['rooms']) - 1:
                                    sol.properties['room_search'] += 1
                                else:
                                    sol.properties['time_slot_index'] += 1
                                    sol.properties['room_search'] = 0
            
                                return self
                            
                    # if new sol has also no solution, problem has no solution
                    print("ERROR, NO SOLUTION PRESENT")
                    sys.exit(1)
            
            print("SOLVED, BE HAPPY :D")
            # just in case
            return self

    def cost(self):
        # TODO: return something different
        return self.preference

    def does_violate_constraint(self):
        # TODO: implement after backtracking is working
        return False
    
    def _find_initial_solution(self):
        result = {}
        for k, uc in self.state['classes'].items():
            uid = uc.uid
            uc = uc.properties
            if uc['committed'] == "true":
                time_slot = uc['time_slots'][0]
                for index, day in enumerate(time_slot['days']):
                    if day == '1':
                        if index == 0:
                            day = Day.Monday
                        elif index == 1:
                            day = Day.Tuesday
                        elif index == 2:
                            day = Day.Wednesday
                        elif index == 3:
                            day = Day.Thursday
                        else:
                            day = Day.Friday

                        if len(uc['rooms']) > 0:
                            event = Event(day, time_slot['start'], time_slot['length'], uc['rooms'][0]['id'], uid)
                            if uid in result:
                                result[uid].append(event)
                            else:
                                result[uid] = [event]
                        else:
                            uc['time_slot_index'] = 0
                            uc['room_index'] = 0
                            uc['room_search'] = 0
                            uc['time_search'] = 0
                            uc['phase1'] = True
                                
            else:
                uc['time_slot_index'] = 0
                uc['room_index'] = 0
                uc['room_search'] = 0
                uc['time_search'] = 0
                uc['phase1'] = True

        return result
