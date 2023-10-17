
import numpy as np
import networkx as nx



class Instance:

    def __init__(self, file_path=None):
        if file_path is None:
            print('No file path was provided')
            return

        instance_type = file_path.split('/')[2]

        if instance_type == 'rail':
            self.cover_matrix, self.cost_vector = load_rail_instance(file_path)
        elif instance_type == 'scp-clr' or instance_type == 'scp-cyc':
            self.cover_matrix, self.cost_vector = load_scp_instance(file_path)
        elif instance_type == 'sts':
            self.cover_matrix, self.cost_vector = load_sts_instance(file_path)
        else:
            raise Exception('Invalid file path')

    def set_cover_matrix(self, cover_matrix):
        self.cover_matrix = cover_matrix

    def set_cost_vector(self, cost_vector):
        self.cost_vector = cost_vector

    def subset_size_features(self):
        subset_sizes = np.sum(self.cover_matrix, axis=0)

        # Get the number of columns
        num_subsets = self.cover_matrix.shape[1]

        normed_subset_sizes = subset_sizes / num_subsets

        return \
        np.mean(normed_subset_sizes), \
        np.std(normed_subset_sizes), \
        np.median(np.absolute(normed_subset_sizes - np.median(normed_subset_sizes))), \
        np.min(normed_subset_sizes), \
        np.quantile(normed_subset_sizes, 0.25), \
        np.median(normed_subset_sizes), \
        np.quantile(normed_subset_sizes, 0.75), \
        np.max(normed_subset_sizes)

    def subset_size_cost_ratio_features(self):
        subset_sizes = np.sum(self.cover_matrix, axis=0)

        # Get the number of columns
        num_subsets = self.cover_matrix.shape[1]

        normed_subset_sizes = subset_sizes / num_subsets
        normed_costs = self.cost_vector / sum(self.cost_vector)
        subset_size_cost_ratio = normed_subset_sizes / normed_costs 

        return \
        np.mean(subset_size_cost_ratio), \
        np.std(subset_size_cost_ratio), \
        np.median(np.absolute(subset_size_cost_ratio - np.median(subset_size_cost_ratio))), \
        np.min(subset_size_cost_ratio), \
        np.quantile(subset_size_cost_ratio, 0.25), \
        np.median(subset_size_cost_ratio), \
        np.quantile(subset_size_cost_ratio, 0.75), \
        np.max(subset_size_cost_ratio)

    def num_of_appearances_features(self):
        element_appearances = np.sum(self.cover_matrix, axis=1)

        # Get the number of columns
        num_subsets = self.cover_matrix.shape[1]

        # Appearances are normed to be comparable accross multiple instances
        normed_appearances = element_appearances / num_subsets

        return \
        np.mean(normed_appearances), \
        np.std(normed_appearances), \
        np.median(np.absolute(normed_appearances - np.median(normed_appearances))), \
        np.min(normed_appearances), \
        np.quantile(normed_appearances, 0.25), \
        np.median(normed_appearances), \
        np.quantile(normed_appearances, 0.75), \
        np.max(normed_appearances)

    def cost_feature(self):
        # Costs are normed to be comparable accross multiple instances
        normed_costs = self.cost_vector / sum(self.cost_vector)
        return \
        np.std(normed_costs), \
        np.median(np.absolute(normed_costs - np.median(normed_costs))), \
        np.quantile(normed_costs, 0.75) - np.quantile(normed_costs, 0.25)

    def forced_set_feature(self):
        element_appearances = np.sum(self.cover_matrix, axis=1)
        # Count the number of elements that appaear in only one set
        return np.count_nonzero(element_appearances == 1)

    def calc_graph(self):
        adjacency_matrix = np.zeros((self.cover_matrix.shape[0], self.cover_matrix.shape[0]))
        for col_idx in range(self.cover_matrix.shape[1]):
            column = self.cover_matrix[:, col_idx]
            elems = np.where(column == 1)[0]
            for e1 in elems:
                for e2 in elems:
                    if e1 != e2:
                        adjacency_matrix[e1, e2] = 1
                        adjacency_matrix[e2, e1] = 1

        return adjacency_matrix
    
    def graph_features(self):
        adjacency_matrix = self.calc_graph()
        graph = nx.from_numpy_array(adjacency_matrix)

        nx.draw(graph, with_labels=True, node_color='lightblue', node_size=50, font_size=12, font_weight='bold', width=2)


        connected_components = list(nx.connected_components(graph))
        cycles = list(nx.simple_cycles(graph))
        shortest_cycle = min(cycles, key=len)
        longest_cycle = max(cycles, key=len)
        
        return \
        len(connected_components), \
        len(shortest_cycle), \
        len(longest_cycle)



def load_rail_instance(file_path):
    with open(file_path, 'r') as file:
        for col_idx, line in enumerate(file, start=-1):
            line = line.lstrip().rstrip('\n').rstrip(' ').split(' ')

            # First line contains dimensions
            if col_idx == -1:
                shape = tuple(int(x) for x in line)
                cover_matrix = np.zeros(shape, dtype=np.int64)
                cost_vector = np.zeros(shape[1], dtype=np.int64)
                continue
            # First entry in row is cost of subset
            cost_vector[col_idx] = int(line[0])

            # Also skip second entry since it just states how many elements are covered by the subset
            for i in range(2, len(line)):
                element = int(line[i])

                # elements begin at 1 therfore we subtract 1 for obtaining its index
                cover_matrix[element-1, col_idx] = 1
    return cover_matrix, cost_vector
    
def load_sts_instance(file_path):
    with open(file_path, 'r') as file:
        for col_idx, line in enumerate(file, start=-1):
            line = line.lstrip().rstrip('\n').rstrip(' ').split(' ')

            # First line contains dimensions
            if col_idx == -1:
                shape = tuple(int(x) for x in line)
                cover_matrix = np.zeros(shape, dtype=np.int64)
                cost_vector = np.zeros(shape[1], dtype=np.int64)
                continue

            # STS instances are unicost
            cost_vector[col_idx] = 1

            # Also skip second entry since it just states how many elements are covered by the subset
            for i in range(len(line)):
                element = int(line[i])

                # elements begin at 1 therfore we subtract 1 for obtaining its index
                cover_matrix[element-1, col_idx] = 1
    return cover_matrix, cost_vector


def load_scp_instance(file_path):
    col_idx = -1
    with open(file_path, 'r') as file:
        for idx, line in enumerate(file, start=-1):
            line = line.lstrip().rstrip('\n').rstrip(' ').split(' ')

            # First line contains dimensions
            if idx == -1:
                line.reverse()

                # Because number of subsets is first in this format we need to reverse 
                shape = tuple(int(x) for x in line)
                cover_matrix = np.zeros(shape, dtype=np.int64)
                cost_vector = np.zeros(shape[1], dtype=np.int64)
                continue

            if all(element == '1' for element in line) or len(''.join(line)) == 0:
                continue

            if len(line) == 1:
                # costs are specified right before subset elements
                col_idx += 1
                cost_vector[col_idx] = int(line[0])
                continue

            # Also skip second entry since it just states how many elements are covered by the subset
            for i in range(len(line)):
                element = int(line[i])

                # elements begin at 1 therfore we subtract 1 for obtaining its index
                cover_matrix[element-1, col_idx] = 1
    return cover_matrix, cost_vector

