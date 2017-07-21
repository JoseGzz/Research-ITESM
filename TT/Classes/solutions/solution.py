# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class Solution(metaclass=ABCMeta):
    @property
    def moved(self):
        return self._moved
    
    @moved.setter
    def moved(self, new_moved):
        self._moved = new_moved
    
    def __init__(self):
        self._moved = 0
        
    @abstractmethod
    def permute(self, heuristic):
        pass

    @abstractmethod
    def does_violate_constraint(self):
        pass

    @abstractmethod
    def cost(self):
        pass
