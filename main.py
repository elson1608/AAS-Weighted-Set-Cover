from instances.instance import Instance, generate
from solvers.nuwls import NuWLSSolver
import time

if __name__ == "__main__":
     # assign_new_costs('rail516', 0.1)
     # assign_new_costs('sts-9', 0.1)
     # assign_new_costs('scpnre1', 0.1)
     # assign_new_costs('scpcyc-06', 0.1)
     # assign_new_costs('scpclr-10', 0.1)
     # assign_new_costs('scp41', 0.1)
     # instance = Instance('sts-9')
     # solver = NuWLSSolver()
     # elapsed_time, solution_cost = solver.solve(instance, 10)
     # print('done')
     # solve_NuWLS(instance, 10)
     # solve_cplex(instance)

     instance = Instance('scp42')
     instance.assign_new_costs_margin(0.5)
     # instance = Instance('AAS-Weighted-Set-Cover/instances/scp-clr/scpclr10.txt')
     # instance = Instance('AAS-Weighted-Set-Cover/instances/scp-cyc/scpcyc06.txt')
     