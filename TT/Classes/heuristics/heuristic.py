# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from solutions.solution import Solution


class Heuristic(metaclass=ABCMeta):
    @abstractmethod
    def permute(self, solution: Solution):
        pass
