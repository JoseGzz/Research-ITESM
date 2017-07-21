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
    
    def find_room(self, ci):
        room = None
        if len(ci.properties['rooms']) > 0 and ci.properties['room_index'] < len(ci.properties['rooms']):
            room = ci.properties['rooms'][ci.properties['room_index']]['id']
            room = self.state['rooms'][room]
        # else:
        #     for rk, r in self.state['rooms'].items():
        #         conflict = True
        #         for ek, event in self.solution_space.items():
        #             if event.day == day and event.room == r.uid and \
        #                     (time_slot['start_time'] < event.start_time + event.duration
        #                     and time_slot['start_time'] + time_slot['length'] > event.start_time):
        #                 pass
        #             else:
        #                 conflict = False
        #                 break
        #
        #         if not conflict:
        #             room = r
        #             break
        
        return room
    
    def is_feasible(self, sol, days, room, time_start, time_length):
        for day in days:
            event = Event(day, time_start, time_length, room.uid, sol.uid)
            if SameRoomAndTime().is_violated(self, event) or \
                                    SameStudents().is_violated(self, event):
                return False
            
        return True
        
    def permute(self, heuristic):
        # do the backtracking and return a new solution
        if self.isBacktracking:
            failed = False
            for k, sol in self.state['classes'].items():
                # TODO: remove thing after and, it should only be not committed
                if sol.properties['committed'] == "false" and len(sol.properties['rooms']) > 0:
                    time_slot = sol.properties['time_slots'][sol.properties['time_slot_index']]
                    days = []
                    for index, day in enumerate(time_slot['days']):
                        if day == '1':
                            days.append(self._get_day(index))

                    room = self.find_room(sol)
                    
                    if room is None:
                        failed = True
                        
                    if (not failed) and self.is_feasible(sol, days, room,time_slot['start'], time_slot['length']):
                        self.solution_space[sol.uid] = []
                        
                        for day in days:
                            self.solution_space[sol.uid].append(Event(day, time_slot['start'],
                                                         time_slot['length'], room.uid, sol.uid))
                            sol.properties['committed'] = "true"
                            rooms = self.state['rooms']
    
                            room_index = 0
                            for i, r in rooms.items():
                                if r.uid == room:
                                    break
                                    
                                room_index += 1
                            print("succeded {0}-{1}, {2}-{3}".format(day, room_index, time_slot['start'],
                                                                 time_slot['length']))

                        self.stack.append(self.solution_space[sol.uid])
                    else:
                        if 'room_index' in sol.properties:
                            if sol.properties['room_index'] < len(sol.properties['rooms']) - 1:
                                sol.properties['room_index'] += 1
                            else:
                                sol.properties['room_index'] = 0
                                sol.properties['time_slot_index'] += 1
                                
                                if sol.properties['time_slot_index'] >= len(sol.properties['time_slots']):
                                    if len(self.stack) > 0:
                                        events = self.stack.pop()
                                        new_sol = self.state['classes'][events[0].uid]
                                        new_sol.properties['committed'] = "false"

                                        if 'room_index' in new_sol.properties:
                                            if new_sol.properties['room_index'] < len(new_sol.properties['rooms']) - 1:
                                                new_sol.properties['room_index'] += 1
                                            else:
                                                new_sol.properties['room_index'] = 0
                                                new_sol.properties['time_slot_index'] += 1
                                                
                                                if new_sol.properties['time_slot_index'] >= \
                                                    len(new_sol.properties['time_slots']):
                                                    print("ERROR 1")
                                                    sys.exit(1)
                                    else:
                                        print("ERROR 2")
                                        sys.exit(1)
                                     
                        print("failed")
                    
                    return self
                            
            # just in case
            return self

    def cost(self):
        # TODO: return something different
        return 0

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
                if len(uc['rooms']) > 0:
                    uc['room_index'] = 0
                        
        return result
