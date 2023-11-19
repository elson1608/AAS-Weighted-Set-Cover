from solver import Solver
import gurobipy as gp
from gurobipy import GRB



class GurobiSolver(Solver):
    
    def solve(self, instance, time_limit):
        cover_matrix = instance.cover_matrix
        cost_vector = instance.cost_vector
        model = gp.Model("set_cover")
        model.setParam('TimeLimit', time_limit)

        # Variables to determine which subsets are chosen
        choices = model.addMVar(shape=(cover_matrix.shape[1],), vtype=GRB.BINARY, name="choices")

        # Constraint that ensures that every element of the universe set is covered
        model.addConstrs(
            (cover_matrix[i, :] @ choices >= 1 for i in range(cover_matrix.shape[0])), name="cover_element"
        )

        # Objective to minimize the cost of the chosen subsets
        model.setObjective(
            cost_vector @ choices, GRB.MINIMIZE
        )

        model.update()

        model.optimize()

        elapsed_time = model.Runtime
        solution_cost = cost_vector @ choices.X 

        return elapsed_time, solution_cost