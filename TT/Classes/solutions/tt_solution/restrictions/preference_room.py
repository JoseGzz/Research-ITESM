from TT.Classes.solutions.tt_solution.restrictions.soft_restriction import SoftRestriction


class PreferenceRoom(SoftRestriction):
    def cost(self, solution, e) -> float:
        uc = solution.state['classes'][e.uid]

        for room in uc.properties['rooms']:
            if room['id'] == e.room:
                return 0.0

        return 10.0
