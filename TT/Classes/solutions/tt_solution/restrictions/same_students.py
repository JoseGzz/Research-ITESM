from TT.Classes.solutions.tt_solution.restrictions.restriction import Restriction


class SameStudents(Restriction):
    def is_violated(self, solution, e) -> bool:
        uc = solution.state["classes"][e.uid]
        events = solution.solution_space
        
        if "SAME_STUDENTS" in uc.properties['constraints']:
            related_classes_ids = uc.properties['constraints']["SAME_STUDENTS"]
            
            for related_class_id in related_classes_ids:
                if related_class_id in events:
                    event_list = events[related_class_id]
                    
                    for event in event_list:
                        if event.day == e.day:
                            if (e.start_time < event.start_time + event.duration and
                                            e.start_time + e.duration > event.start_time):
                                print("students broken by {0} and {1}".format(e.uid, event.uid))
                                return True
        
        return False
