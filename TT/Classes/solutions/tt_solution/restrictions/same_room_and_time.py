from TT.Classes.solutions.tt_solution.restrictions.restriction import Restriction


class SameRoomAndTime(Restriction):
    def is_violated(self, solution, e) -> bool:
        events = solution.solution_space

        for ek, event_list in events.items():
            for event in event_list:
                if event == e:
                    continue
                if event.day == e.day:
                    if event.room == e.room:
                        if (e.start_time < event.start_time + event.duration and
                                e.start_time + e.duration > event.start_time):
                            return True
        
        return False
