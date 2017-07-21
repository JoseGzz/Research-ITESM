# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from solutions.solution import Solution


class HyperHeuristic(metaclass=ABCMeta):
    @property
    def solver(self):
        return self._solver
    
    @property
    def iteration(self):
        return self._iteration
    
    @solver.setter
    def solver(self, new_solver):
        self._solver = new_solver
        
    @iteration.setter
    def iteration(self, new_iteration):
        self._iteration = new_iteration
        
    def __init__(self):
        self._solver = None
        self._iteration = 0
        
    @abstractmethod
    def get_heuristic(self, current_solution: Solution):
        pass
    
    @abstractmethod
    def register(self, solver):
        self.solver = solver

    def add_best_makespan(self, cost: float):
        pass
