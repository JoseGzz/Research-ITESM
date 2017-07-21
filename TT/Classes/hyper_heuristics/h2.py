# -*- coding: utf-8 -*-
from .hyper_heuristic import HyperHeuristic
from solutions.solution import Solution
from heuristics.qap_heuristics import BestMove
from heuristics.qap_heuristics import ReverseSequentialSearch
from heuristics.qap_heuristics import DoubleExchange
from heuristics.qap_heuristics import PredecessorAndSuccessor


class H2(HyperHeuristic):
    def __init__(self):
        super(H2, self).__init__()
        self.prev_best_makespans = []
        self.iteration = 0
        self.last_heuristic_change = 0
        self.heuristic = None
        self.seq_counter = 0
        self.custom_temp = 100
        self.limit = 20
        self.first_makespan = 0
        self.state = "START"
    
    def register(self, solver):
        self.solver = solver
        self.heuristic = PredecessorAndSuccessor(solver)
    
    def get_heuristic(self, current_solution: Solution):
        if self.iteration < 100 and (isinstance(self.heuristic, PredecessorAndSuccessor)
                                     or isinstance(self.heuristic, DoubleExchange)
                                     or isinstance(self.heuristic, ReverseSequentialSearch)):
            if not self.was_there_change():
                if isinstance(self.heuristic, PredecessorAndSuccessor):
                    self.heuristic = DoubleExchange(self.solver)
                    self.limit = 15
                    self.prev_best_makespans = []
                else:
                    self.heuristic = PredecessorAndSuccessor(self.solver)
                    self.limit = 15
                    self.prev_best_makespans = []
            
            if self.iteration > 30 and len(self.prev_best_makespans) > 0:
                if self.prev_best_makespans[-1] - self.first_makespan == 0:
                    self.heuristic = ReverseSequentialSearch(self.solver)
                    self.limit = 5
                    self.prev_best_makespans = []
            
            return self.heuristic
        elif self.state == "START" and (isinstance(self.heuristic, PredecessorAndSuccessor)
                                        or isinstance(self.heuristic, DoubleExchange)
                                        or isinstance(self.heuristic, ReverseSequentialSearch)):
            self.last_heuristic_change = 0
            self.heuristic = BestMove(3, self.solver)
            self.solver.temp = 100
            self.iteration = 0
            self.solver.eiter = 0
            self.limit = 15
            self.prev_best_makespans = []
            self.state = "END"
            return self.heuristic
        
        if isinstance(self.heuristic, BestMove):
            if (self.iteration - self.last_heuristic_change) < 70:
                if self.was_there_change():
                    return self.heuristic
                else:
                    self.last_heuristic_change = self.iteration
                    self.heuristic = ReverseSequentialSearch(self.solver)
                    self.seq_counter = 1
                    self.prev_best_makespans = []
                    self.limit = 6
                    
                    return self.heuristic
            else:
                self.last_heuristic_change = self.iteration
                self.heuristic = ReverseSequentialSearch(self.solver)
                self.seq_counter = 1
                
                return self.heuristic
        
        if isinstance(self.heuristic, ReverseSequentialSearch):
            if self.seq_counter < 5:
                self.seq_counter += 1
                return self.heuristic
            else:
                self.last_heuristic_change = self.iteration
                self.heuristic = BestMove(3, self.solver)
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
