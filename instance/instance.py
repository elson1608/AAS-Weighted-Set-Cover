from .generator import *

class Instance:
    def __init__(self, universe_size, n_subsets) -> None:
        self.subsets, self.costs = generate_instance(universe_size, n_subsets)