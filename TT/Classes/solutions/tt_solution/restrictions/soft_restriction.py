from abc import ABCMeta, abstractmethod


class SoftRestriction(metaclass=ABCMeta):
    @abstractmethod
    def cost(self, solution, e) -> float:
        pass
