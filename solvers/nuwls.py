import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solvers.solver import Solver
import os
import subprocess

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
        res = subprocess.run(f"grep 'o' {out_path} | tail -n 1", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        elapsed_time = float(res.stdout.split('/')[0])
        solution_cost = float(res.stdout.split(' ')[1])

        # clean up 
        os.system(f"rm -f {out_path}")
        os.system(f"rm -f {var_path}")
        os.system(f"rm -f {wat_path}")

        return elapsed_time, solution_cost