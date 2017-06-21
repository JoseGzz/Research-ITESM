from abc import ABCMeta, abstractmethod


class Heuristic(metaclass=ABCMeta):
    @abstractmethod
    def perturb_solution(self, current_solution):
        pass
