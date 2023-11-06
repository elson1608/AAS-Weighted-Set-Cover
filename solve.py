import gurobipy as gp
from gurobipy import GRB
import numpy as np
import time
import cplex
import os
import subprocess

cplex_start_time = None
elapsed_time = None



def solve_gurobi(instance, time_limit):
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

    print(model.Runtime)
    return elapsed_time, solution_cost

class TimeCallback(cplex.callbacks.IncumbentCallback):
    def __call__(self) -> None:
        global cplex_start_time
        global elapsed_time 
        elapsed_time = self.get_time() - cplex_start_time

def solve_cplex(instance, time_limit):
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

    model.register_callback(TimeCallback)
    model.parameters.timelimit.set(time_limit)

    # Record the start time (CPU time)
    global cplex_start_time 
    cplex_start_time = time.time()

    model.solve()


    global elapsed_time
    elapsed_time = "{:.2f}".format(elapsed_time)
    solution_cost = model.solution.get_objective_value() 

    return elapsed_time, solution_cost


def solve_NuWLS(instance, time_limit):
    solver_path = 'wncf-solvers/NuWLS-c-2023'
    run = os.path.join(solver_path, 'run')
    executable =  os.path.join(solver_path, 'NuWLS-c_static')
    out_path = os.path.join(solver_path, 'output.out')
    var_path = os.path.join(solver_path, 'output.var')
    wat_path = os.path.join(solver_path, 'output.wat')
    
    # run solver
    os.system(f"{run} --timestamp -d 15 -o {out_path} -v {var_path} -w {wat_path} -C {time_limit} -W {time_limit} -M {32768} {executable} {instance.wcnf_path}")
    
    # get results from out file
    res = subprocess.run(f"grep 'o' {out_path} | tail -n 1", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    elapsed_time = float(res.stdout.split('/')[0])
    solution_cost = float(res.stdout.split(' ')[1])
    
    # clean up 
    os.system(f"rm -f {out_path}")
    os.system(f"rm -f {var_path}")
    os.system(f"rm -f {wat_path}")

    return elapsed_time, solution_cost
