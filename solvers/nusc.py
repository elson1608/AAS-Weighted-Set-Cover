from solver import Solver
import os

class NuSCSolver(Solver):
    
    def solve(self, instance, time_limit):
        solver_path = 'solvers/NuSC'
        executable =  os.path.join(solver_path, 'NuSC')
