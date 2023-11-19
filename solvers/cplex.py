from solver import Solver
import cplex
import time

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


        elapsed_time = "{:.2f}".format(elapsed_time)
        solution_cost = model.solution.get_objective_value() 

        return elapsed_time, solution_cost