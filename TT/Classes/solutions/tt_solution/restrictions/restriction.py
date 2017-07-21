from abc import ABCMeta, abstractmethod


class Restriction(metaclass=ABCMeta):
    @abstractmethod
    def is_violated(self, solution, e) -> bool:
        pass
