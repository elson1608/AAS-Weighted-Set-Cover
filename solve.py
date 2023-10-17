import gurobipy as gp
from gurobipy import GRB
import numpy as np
import time
import cplex


def solve_gurobi(instance):
    cover_matrix = instance.cover_matrix
    cost_vector = instance.cost_vector
    model = gp.Model("set_cover")
    model.setParam('TimeLimit', 10)
    
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
    
    # Record the start time (CPU time)
    # start_time = time.perf_counter_ns()
    

    model.optimize()

    
    # Record the end time (CPU time)
    # end_time = time.perf_counter_ns()

    solution_time = model.Runtime
    solution_cost = cost_vector @ choices.X 

    print(model.Runtime)
    return solution_time, solution_cost

def solve_cplex(instance):
    cover_matrix = instance.cover_matrix.astype(float)
    cost_vector = instance.cost_vector.astype(float)
    model = cplex.Cplex()
    

    model.variables.add(
        obj=cost_vector,
        types="B" * cover_matrix.shape[1]
    )

    # Constraint that ensures that every element of the universe set is covered
    # left hand side, sum over j x_j * a_ij for all i
    constraints = [[range(cover_matrix.shape[1]), list(cover_matrix[i, :])] for i in range(cover_matrix.shape[0])]
    
    # >=
    constraint_senses = "G" * cover_matrix.shape[0]
    
    # right hand side, 1 
    rhs = [1] * cover_matrix.shape[0]


    model.linear_constraints.add(
        lin_expr=constraints,
        senses=constraint_senses,
        rhs=rhs
    )

    model.objective.set_name("cost")
    model.objective.set_sense(model.objective.sense.minimize)


    model.parameters.timelimit.set(10)

    # Record the start time (CPU time)
    start_time = time.perf_counter_ns()
    
    model.solve()
    


    # Record the end time (CPU time)
    end_time = time.perf_counter_ns() 
    
    # Print the solution


    solution_time = end_time - start_time
    solution_cost = model.solution.get_objective_value() 

    return solution_time, solution_cost


def solve_minizinc():
    pass