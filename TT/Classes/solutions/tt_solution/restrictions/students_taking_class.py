from TT.Classes.solutions.tt_solution.restrictions.soft_restriction import SoftRestriction


class StudentsTakingClass(SoftRestriction):
    def cost(self, solution, e) -> float:
        ur = solution.state['rooms'][e.room]
        cap = int(ur.properties['capacity'])
        
        if e.uid not in solution.state['enrollments']:
            return 0.0
        
        enrolled = solution.state['enrollments'][e.uid]
        
        print("{0} - {1}".format(len(enrolled), cap/2))
        if cap/2 >= len(enrolled):
            return 0.0
        else:
            return (len(enrolled) - cap/2) * 2
