from solvers.solver import Solver
import os
import subprocess
import random

class NuSCSolver(Solver):
    
    def solve(self, instance, time_limit):
        solver_path = 'solvers/NuSC'
        executable =  os.path.join(solver_path, 'NuSC')

        # run solver
        output = subprocess.run(f"{executable} {instance.txt_path} {time_limit} {random.randint(-(2**31), 2**31 - 1)}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)

        # get results from output
        res = next((line for line in reversed(output.stdout.split('\n')) if line.startswith('o')), None)
        elapsed_time = float(res.split(' ')[2])
        solution_cost = int(res.split(' ')[1])

        return elapsed_time, solution_cost