from abc import ABC, abstractmethod


class Solver(ABC):

    @abstractmethod
    def solve(self, instance, time_limit):
        pass