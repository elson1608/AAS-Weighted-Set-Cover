from solvers.solver import Solver
import gurobipy as gp
from gurobipy import GRB, GurobiError
import numpy as np



class GurobiSolver(Solver):
    
    def solve(self, instance, time_limit):
        with gp.Env(empty=True) as env:
            env.setParam('OutputFlag', 0)
            env.start()
            with gp.Model("set_cover", env=env) as model:
                cover_matrix = instance.cover_matrix
                cost_vector = instance.cost_vector
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
                try: 
                    solution_cost = int(cost_vector @ choices.X) 
                except GurobiError as e:
                    if e.errno == 10005:
                        solution_cost = np.nan

                return elapsed_time, solution_cost