from instance.generator import *
from algorithms.greedy import *


if __name__ == "__main__":
    instance = Instance(25, 5)
    print("instance:")
    #print(instance)
    algorithm = Greedy()
    algorithm.solve(instance)
    algorithm.print_solution()