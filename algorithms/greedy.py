from instance.instance import * 
import numpy as np
import pprint
from .algorithm import *
from utils import neg


class Greedy(Algorithm):

    def __init__(self) -> None:
        self.solution = None

    def solve(self, instance: Instance):
        all_subsets = np.copy(instance.subsets)
        remaining = np.array([1] * len(instance.subsets))
        solution_sets = []
        solution_cost = 0
        while np.any(remaining):
            best = (float('inf'), 0)
            for j in range(len(instance.subsets.T)):
                subset = instance.subsets[:, j]
                uncovered = remaining & subset
                cost = instance.costs[j]
                print(uncovered)
                print(sum(uncovered))
                heuristic = cost / sum(uncovered)

                if heuristic < best[0]:
                    best = (heuristic, j)

            selected_column = best[1] 
            solution_sets.append(selected_column)
            solution_cost = solution_cost + instance.costs[selected_column] 
            remaining = remaining & neg(instance.subsets[:, selected_column])
            instance.subsets = np.delete(instance.subsets, selected_column, 1)
            instance.costs = np.delete(instance.costs, selected_column)

        self.solution =  {"all_subsets": all_subsets, "solution_sets": solution_sets, "solution_cost": solution_cost}


    def print_solution(self):
        subsets_to_print = []
        for j in self.solution["solution_sets"]:
            selected_subset = [i for i in range(len(self.solution["all_subsets"])) if 1 == self.solution["all_subsets"][i, j]]
            subsets_to_print.append(selected_subset)
        print("selected subsets:")
        print(pprint.pformat(subsets_to_print, compact=True))
        print("with a cost of:")
        print(self.solution["solution_cost"])