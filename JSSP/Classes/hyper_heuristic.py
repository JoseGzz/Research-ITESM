from solution import Solution

class HyperHeuristic1:
    prev_best_makespans = []
    iteration = 0
    last_heuristic_change = 0
    heuristic = "P_AND_S"
    seq_counter = 0
    set_temp = False
    custom_temp = 100
    
    def heursitic_to_use(self):
        if self.iteration < 100:
            return self.heuristic
        elif self.heuristic == "P_AND_S":
            self.last_heuristic_change = 0
            self.heuristic = "BEST"
            self.set_temp = True
            return self.heuristic
        
        if self.heuristic == "BEST":
            if (self.iteration - self.last_heuristic_change) < 70:
                if self.was_there_change():
                    return self.heuristic
                else:
                    self.last_heuristic_change = self.iteration
                    self.heuristic = "SEQUENTIAL"
                    self.seq_counter = 1
                    return self.heuristic
            else:
                self.last_heuristic_change = self.iteration
                self.heuristic = "SEQUENTIAL"
                self.seq_counter = 1
                return self.heuristic
            
        if self.heuristic == "SEQUENTIAL":
            if self.seq_counter < 5:
                self.seq_counter += 1
                return self.heuristic
            else:
                self.last_heuristic_change = self.iteration
                self.heuristic = "BEST"
                return self.heuristic
            
    def was_there_change(self):
        if len(self.prev_best_makespans) < 15:
            return True
        
        current_makespan = self.prev_best_makespans[0]
        for makespan in self.prev_best_makespans:
            if current_makespan != makespan:
                return True
            
        return False

    def add_best_makespan(self, new_makespan):
        if len(self.prev_best_makespans) < 15:
            self.prev_best_makespans.append(new_makespan)
        else:
            self.prev_best_makespans.pop(0)
            self.prev_best_makespans.append(new_makespan)
