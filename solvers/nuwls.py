import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solvers.solver import Solver
import os
import numpy as np

class NuWLSSolver(Solver):
    
    def solve(self, instance, time_limit):
        solver_path = 'solvers/NuWLS-c-2023'
        run = os.path.join(solver_path, 'run')
        executable =  os.path.join(solver_path, 'NuWLS-c_static')
        out_path = os.path.join(solver_path, 'output.out')
        var_path = os.path.join(solver_path, 'output.var')
        wat_path = os.path.join(solver_path, 'output.wat')

        # run solver
        os.system(f"{run} --timestamp -d 15 -o {out_path} -v {var_path} -w {wat_path} -C {time_limit} -W {time_limit} -M {32768} {executable} {instance.wcnf_path}")

        # get results from out file
        last_line = ''
        with open(out_path, 'r') as file:
            lines = file.readlines()  # reads all lines into a list
            for line in lines:
                if 'UNKNOWN' in line:
                    elapsed_time = float(last_line.split('/')[0])
                    solution_cost = np.nan
                    break
                if 'NuWLS search done!' in line or 'SATISFIABLE' in line:
                    elapsed_time = float(last_line.split('/')[0])
                    solution_cost = int(last_line.split(' ')[-1])
                    break
                last_line = line 

        # clean up 
        os.system(f"rm -f {out_path}")
        os.system(f"rm -f {var_path}")
        os.system(f"rm -f {wat_path}")

        return elapsed_time, solution_cost