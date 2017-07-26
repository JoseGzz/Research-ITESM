from TT.Classes.solutions.tt_solution.restrictions.restriction import Restriction


class Spread(Restriction):
    def is_violated(self, solution, e) -> bool:
        uc = solution.state["classes"][e.uid]
        events = solution.solution_space
        
        if "SPREAD" in uc.properties['constraints']:
            related_classes_ids = uc.properties['constraints']["SPREAD"]
            
            for related_class_id in related_classes_ids:
                if related_class_id in events:
                    event_list = events[related_class_id]
                    
                    for event in event_list:
                        if event.uid == e.uid:
                            continue
                        if (e.start_time < event.start_time + event.duration and
                                        e.start_time + e.duration > event.start_time):
                            print("spread broken by {0} and {1}".format(e.uid, event.uid))
                            return True
        
        return False
