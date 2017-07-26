from TT.Classes.solutions.tt_solution.restrictions.restriction import Restriction


class Precedence(Restriction):
    def is_violated(self, solution, e) -> bool:
        uc = solution.state["classes"][e.uid]
        events = solution.solution_space
        
        if "PRECEDENCE" in uc.properties['constraints']:
            related_classes_ids = uc.properties['constraints']["PRECEDENCE"]
            
            for related_class_id in related_classes_ids:
                if related_class_id in events:
                    event_list = events[related_class_id]
                    
                    for i in range(len(event_list) - 1):
                        earlier_event = event_list[i]
                        later_event = event_list[i + 1]
                        
                        if later_event.start_time < earlier_event.start_time + earlier_event.duration:
                            print("precedence broken by {0} and {1}".format(earlier_event.uid, later_event.uid))
                            return True
        
        return False
