from TT.Classes.solutions.tt_solution.restrictions.soft_restriction import SoftRestriction


class RoomCost(SoftRestriction):
    def cost(self, solution, e) -> float:
        uc = solution.state['classes'][e.uid]
        
        for room in uc.properties['rooms']:
            if 'pref' in room:
                if room['id'] == e.room:
                    return float(room['pref'])
        
        return 0.0
