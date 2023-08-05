import random
import sys
import numpy as np


# returns a set cover instance (subsets, costs)
# universe_size: number of elements in the univers
# n_subsets: number of subsets to be created
# subsets is a matrix with universe_size rows and n_subsets columns
# it contains a 1 at position (i,j) if i is included in the j-th subset 
def generate_instance(universe_size, n_subsets):
    # generate universe set containing universe_size numbers from [0, max_elem) 
    universe_set = list(range(universe_size))
    
    # generate n_subsets
    subsets = np.empty((25, 0), dtype=int)
    remaining = np.array([1] * universe_size, dtype=int)
    for i in range(n_subsets-1):
        subset_size = random.randint(1, len(universe_set))
        subset = random.sample(sorted(universe_set), subset_size)
        subset = np.array([1 if e in subset else 0 for e in universe_set], dtype=int)
        subsets = np.column_stack((subsets, subset))
        remaining = remaining ^ subset

    # make sure that instance is solvable
    if np.any(remaining):
        subsets = np.column_stack((subsets, remaining))
    else:
        subset_size = random.randint(1, len(universe_set))
        subset = random.sample(sorted(universe_set), subset_size)
        subset = np.array([1 if e in subset else 0 for e in universe_set], dtype=int)
        subsets = np.column_stack((subsets, subset))

    # assign costs to each subset
    costs = [random.random() for j in range(n_subsets)]

    # costs are normalized s.t. their sum equals 1
    costs = np.array([e / sum(costs) for e in costs])

    return subsets, costs