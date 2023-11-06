from instance import Instance, assign_new_costs
from solve import solve_cplex, solve_NuWLS
import time

if __name__ == "__main__":
     assign_new_costs('rail516', 0.1)
     # instance = Instance('rail516')
     # solve_NuWLS(instance, 10)
     # solve_cplex(instance)

     # instance = Instance('AAS-Weighted-Set-Cover/instances/sts/data.135')
     # instance = Instance('AAS-Weighted-Set-Cover/instances/scp-clr/scpclr10.txt')
     # instance = Instance('AAS-Weighted-Set-Cover/instances/scp-cyc/scpcyc06.txt')
     pass