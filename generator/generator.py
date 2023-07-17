import random
import sys


# returns a set cover instance (universe, subsets, costs)
# universe_size: number of elements in the univers
# max_elem: elements from [0, max_elem) are sampled into the universe
# n_subsets: number of subsets to be created
def generate_instance(universe_size, max_elem, n_subsets):
    # generate universe set containing universe_size numbers from [0, max_elem) 
    universe_set = set(random.sample([e for e in range(max_elem)], universe_size))
    
    # generate n_subsets
    subsets = []
    remaining = set(universe_set)
    for i in range(n_subsets-1):
        subset_size = random.randint(1, len(universe_set))
        subset = set(random.sample(sorted(universe_set), subset_size))
        subsets.append(subset)
        remaining -= subset

    # make sure that instance is solvable
    if remaining:
        subsets.append(remaining)

    # assign costs to each subset
    costs = [random.random() for j in range(n_subsets)]

    # costs are normalized s.t. their sum equals 1
    costs = [e / sum(costs) for e in costs]
    
    return universe_set, subset, costs

if __name__ == "__main__":
    
    if len(sys.argv) != 4:
        print("USAGE: python generator.py <universe_size> <max_elem> <n_subsets>")
        exit(1)

    print(generate_instance(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])))