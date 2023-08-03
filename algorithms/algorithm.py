from instance.instance import *
from abc import ABC, abstractmethod

class Algorithm(ABC):

    @abstractmethod
    def solve(self, instance: Instance):
        pass


    @abstractmethod
    def print_solution(self):
        pass

