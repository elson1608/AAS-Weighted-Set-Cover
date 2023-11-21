from solvers.solver import Solver
import cplex
from cplex.exceptions import CplexSolverError
import time
import numpy as np

class CplexSolver(Solver):

    cplex_start_time = None
    elapsed_time = None

    class TimeCallback(cplex.callbacks.IncumbentCallback):
        def __call__(self) -> None:
            CplexSolver.elapsed_time = self.get_time() - CplexSolver.cplex_start_time
    
    
    def solve(self, instance, time_limit):
        cover_matrix = instance.cover_matrix.astype(float)
        cost_vector = instance.cost_vector.astype(float)
        model = cplex.Cplex()
        model.set_log_stream(None)
        model.set_error_stream(None)
        model.set_warning_stream(None)
        model.set_results_stream(None)


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

        model.register_callback(self.TimeCallback)
        model.parameters.timelimit.set(time_limit)

        # Record the start time (CPU time) 
        CplexSolver.cplex_start_time = time.time()

        model.solve()

        elapsed_time = "{:.2f}".format(CplexSolver.elapsed_time)
        try:
            solution_cost = int(model.solution.get_objective_value())
        except CplexSolverError as e:
            if e.args[2] == 1217:
                solution_cost = np.nan

        return elapsed_time, solution_cost