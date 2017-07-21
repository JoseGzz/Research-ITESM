from solution import Solution
import settings

class HyperHeuristic1:
    prev_best_makespans = []
    iteration = 0
    last_heuristic_change = 0
    heuristic = "P_AND_S"
    seq_counter = 0
    set_temp = False
    custom_temp = 100
    limit = 20
    first_makespan = 0
    state = "START"
    
    def heursitic_to_use(self):
        if settings.options.function == "H1":
            return self.h1()
        if settings.options.function == "H2":
            return self.h2()
        if settings.options.function == "H3":
            return self.h3()
        if settings.options.function == "H4":
            return self.h4()
        
    def h1(self):
        if self.iteration < 100 and (self.heuristic == "P_AND_S" or self.heuristic == "D_EXCHANGE"
                                     or self.heuristic == "SEQUENTIAL"):
            if not self.was_there_change():
                if self.heuristic == "P_AND_S":
                    self.heuristic = "D_EXCHANGE"
                    self.limit = 15
                    self.prev_best_makespans = []
                else:
                    self.heuristic = "P_AND_S"
                    self.limit = 15
                    self.prev_best_makespans = []
                    
            if self.iteration > 30 and len(self.prev_best_makespans) > 0:
                if self.prev_best_makespans[-1] - self.first_makespan == 0:
                    self.heuristic = "SEQUENTIAL"
                    self.limit = 5
                    self.prev_best_makespans = []
                
            return self.heuristic
        elif self.state == "START" and (self.heuristic == "P_AND_S" or self.heuristic == "D_EXCHANGE"
                                        or self.heuristic == "SEQUENTIAL"):
            self.last_heuristic_change = 0
            self.heuristic = "BEST"
            self.set_temp = True
            self.limit = 15
            self.prev_best_makespans = []
            self.state = "END"
            return self.heuristic
        
        if self.heuristic == "BEST":
            if (self.iteration - self.last_heuristic_change) < 70:
                if self.was_there_change():
                    return self.heuristic
                else:
                    self.last_heuristic_change = self.iteration
                    self.heuristic = "SEQUENTIAL"
                    self.seq_counter = 1
                    self.prev_best_makespans = []
                    self.limit = 6
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
                self.prev_best_makespans = []
                self.limit = 10
                return self.heuristic

        # just in case
        return self.heuristic

    def h2(self):
        if self.iteration < 100 and (self.heuristic == "P_AND_S" or self.heuristic == "D_EXCHANGE"
                                     or self.heuristic == "REVERSE_SEQUENTIAL"):
            if not self.was_there_change():
                if self.heuristic == "P_AND_S":
                    self.heuristic = "D_EXCHANGE"
                    self.limit = 15
                    self.prev_best_makespans = []
                else:
                    self.heuristic = "P_AND_S"
                    self.limit = 15
                    self.prev_best_makespans = []
        
            if self.iteration > 30 and len(self.prev_best_makespans) > 0:
                if self.prev_best_makespans[-1] - self.first_makespan == 0:
                    self.heuristic = "REVERSE_SEQUENTIAL"
                    self.limit = 5
                    self.prev_best_makespans = []
        
            return self.heuristic
        elif self.state == "START" and (self.heuristic == "P_AND_S" or self.heuristic == "D_EXCHANGE"
                                        or self.heuristic == "REVERSE_SEQUENTIAL"):
            self.last_heuristic_change = 0
            self.heuristic = "BEST"
            self.set_temp = True
            self.limit = 15
            self.prev_best_makespans = []
            self.state = "END"
            return self.heuristic
    
        if self.heuristic == "BEST":
            if (self.iteration - self.last_heuristic_change) < 70:
                if self.was_there_change():
                    return self.heuristic
                else:
                    self.last_heuristic_change = self.iteration
                    self.heuristic = "REVERSE_SEQUENTIAL"
                    self.seq_counter = 1
                    self.prev_best_makespans = []
                    self.limit = 6
                    return self.heuristic
            else:
                self.last_heuristic_change = self.iteration
                self.heuristic = "REVERSE_SEQUENTIAL"
                self.seq_counter = 1
                return self.heuristic
    
        if self.heuristic == "REVERSE_SEQUENTIAL":
            if self.seq_counter < 5:
                self.seq_counter += 1
            
                return self.heuristic
            else:
                self.last_heuristic_change = self.iteration
                self.heuristic = "BEST"
                self.prev_best_makespans = []
                self.limit = 10
                return self.heuristic
            
        # just in case
        return self.heuristic

    def h3(self):
        if self.iteration < 100 and (self.heuristic == "P_AND_S" or self.heuristic == "D_EXCHANGE"
                                     or self.heuristic == "SEQUENTIAL"):
            if not self.was_there_change():
                if self.heuristic == "P_AND_S":
                    self.heuristic = "D_EXCHANGE"
                    self.limit = 15
                    self.prev_best_makespans = []
                else:
                    self.heuristic = "P_AND_S"
                    self.limit = 15
                    self.prev_best_makespans = []
        
            if self.iteration > 30 and len(self.prev_best_makespans) > 0:
                if self.prev_best_makespans[-1] - self.first_makespan == 0:
                    self.heuristic = "SEQUENTIAL"
                    self.limit = 5
                    self.prev_best_makespans = []
        
            return self.heuristic
        elif self.state == "START" and (self.heuristic == "P_AND_S" or self.heuristic == "D_EXCHANGE"
                                        or self.heuristic == "SEQUENTIAL"):
            self.last_heuristic_change = 0
            self.iteration = 0
            self.heuristic = "SEQUENTIAL"
            self.set_temp = True
            self.limit = 10
            self.seq_counter = 1
            self.prev_best_makespans = []
            self.state = "END"
            return self.heuristic
    
        if self.heuristic == "BEST":
            if (self.iteration - self.last_heuristic_change) < 70:
                if self.was_there_change():
                    return self.heuristic
                else:
                    self.last_heuristic_change = self.iteration
                    self.heuristic = "SEQUENTIAL"
                    self.seq_counter = 1
                    self.prev_best_makespans = []
                    self.limit = 6
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
                self.prev_best_makespans = []
                self.limit = 10
                return self.heuristic

        # just in case
        return self.heuristic

    def h4(self):
        if self.iteration < 100 and (self.heuristic == "P_AND_S" or self.heuristic == "D_EXCHANGE"
                                     or self.heuristic == "REVERSE_SEQUENTIAL"):
            if not self.was_there_change():
                if self.heuristic == "P_AND_S":
                    self.heuristic = "D_EXCHANGE"
                    self.limit = 15
                    self.prev_best_makespans = []
                else:
                    self.heuristic = "P_AND_S"
                    self.limit = 15
                    self.prev_best_makespans = []
        
            if self.iteration > 30 and len(self.prev_best_makespans) > 0:
                if self.prev_best_makespans[-1] - self.first_makespan == 0:
                    self.heuristic = "REVERSE_SEQUENTIAL"
                    self.limit = 5
                    self.prev_best_makespans = []
        
            return self.heuristic
        elif self.state == "START" and (self.heuristic == "P_AND_S" or self.heuristic == "D_EXCHANGE"
                                        or self.heuristic == "REVERSE_SEQUENTIAL"):
            self.last_heuristic_change = 0
            self.iteration = 0
            self.heuristic = "REVERSE_SEQUENTIAL"
            self.set_temp = True
            self.limit = 10
            self.seq_counter = 1
            self.prev_best_makespans = []
            self.state = "END"
            return self.heuristic
    
        if self.heuristic == "BEST":
            if (self.iteration - self.last_heuristic_change) < 70:
                if self.was_there_change():
                    return self.heuristic
                else:
                    self.last_heuristic_change = self.iteration
                    self.heuristic = "REVERSE_SEQUENTIAL"
                    self.seq_counter = 1
                    self.prev_best_makespans = []
                    self.limit = 6
                    return self.heuristic
            else:
                self.last_heuristic_change = self.iteration
                self.heuristic = "REVERSE_SEQUENTIAL"
                self.seq_counter = 1
                return self.heuristic
    
        if self.heuristic == "REVERSE_SEQUENTIAL":
            if self.seq_counter < 5:
                self.seq_counter += 1
            
                return self.heuristic
            else:
                self.last_heuristic_change = self.iteration
                self.heuristic = "BEST"
                self.prev_best_makespans = []
                self.limit = 10
                return self.heuristic

        # just in case
        return self.heuristic
            
    def was_there_change(self):
        if len(self.prev_best_makespans) < self.limit:
            return True
        
        current_makespan = self.prev_best_makespans[0]
        for makespan in self.prev_best_makespans:
            if current_makespan != makespan:
                return True
            
        return False

    def add_best_makespan(self, new_makespan):
        if len(self.prev_best_makespans) < self.limit:
            self.prev_best_makespans.append(new_makespan)
        else:
            self.prev_best_makespans.pop(0)
            self.prev_best_makespans.append(new_makespan)
