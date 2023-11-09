
import numpy as np
import networkx as nx
import time
from sample import sample
from encode import *


class Instance:

    def __init__(self, file_name=None):
        if file_name.startswith('rail'):
            self.txt_path = 'instances/txt/Rail/' + file_name + '.txt'
            self.wcnf_path = 'instances/wcnf/Rail/' + file_name + '.wcnf'
        elif file_name.startswith('sts'):
            self.txt_path = 'instances/txt/STS/' + file_name + '.txt'
            self.wcnf_path = 'instances/wcnf/STS/' + file_name + '.wcnf'
        elif file_name.startswith('scpn'):
            self.txt_path = 'instances/txt/OR-Large/' + file_name + '.txt'
            self.wcnf_path = 'instances/wcnf/OR-Large/' + file_name + '.wcnf'
        elif file_name.startswith('scpclr'):
            self.txt_path = 'instances/txt/SCP-CLR/' + file_name + '.txt'
            self.wcnf_path = 'instances/wcnf/SCP-CLR/' + file_name + '.wcnf'
        elif file_name.startswith('scpcyc'):
            self.txt_path = 'instances/txt/SCP-CYC/' + file_name + '.txt'
            self.wcnf_path = 'instances/wcnf/SCP-CYC/' + file_name + '.wcnf'
        elif file_name.startswith('scp'):
            self.txt_path = 'instances/txt/OR-Small/' + file_name + '.txt'
            self.wcnf_path = 'instances/wcnf/OR-Small/' + file_name + '.wcnf'


        if self.txt_path is None:
            print('No file path was provided')
            return

        instance_type = self.txt_path.split('/')[-2]

        if instance_type == 'Rail':
            self.cover_matrix, self.cost_vector = load_rail_instance(self.txt_path)
        elif instance_type in ['SCP-CLR', 'SCP-CYC', 'OR-Large', 'OR-Small']:
            self.cover_matrix, self.cost_vector = load_scp_instance(self.txt_path)
        elif instance_type == 'STS':
            self.cover_matrix, self.cost_vector = load_sts_instance(self.txt_path)
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
        return \
        np.std(self.cost_vector) / np.mean(self.cost_vector), \
        np.median(np.absolute(self.cost_vector - np.median(self.cost_vector))) / np.median(self.cost_vector), \
        (np.quantile(self.cost_vector, 0.75) - np.quantile(self.cost_vector, 0.25)) / np.quantile(self.cost_vector, 0.75)

    def forced_set_feature(self):
        element_appearances = np.sum(self.cover_matrix, axis=1)
        # Count the number of elements that appaear in only one set
        return np.count_nonzero(element_appearances == 1)

    def calc_graph(self):
        num_elems = self.cover_matrix.shape[0]
        adjacency_matrix = np.zeros((num_elems, num_elems), dtype=np.uint8)
        for i in range(num_elems):
            for col in self.cover_matrix.T:
                if col[i] == 1:
                    adjacency_matrix[i, :] |= col
                    adjacency_matrix[:, i] |= col

        np.fill_diagonal(adjacency_matrix, 0)
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
                cover_matrix = np.zeros(shape, dtype=np.uint8)
                cost_vector = np.zeros(shape[1], dtype=np.uint8)
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
            line = [c for c in line if c != '']

            # First line contains dimensions
            if col_idx == -1:
                shape = tuple(int(x) for x in line if x != '')
                cover_matrix = np.zeros(shape, dtype=np.uint8)
                cost_vector = np.zeros(shape[1], dtype=np.uint8)
                continue

            # STS instances are unicost per default
            if len(line) == 3:
                cost_vector[col_idx] = 1
            else:
                cost_vector[col_idx] = line[3] 

            for i in range(3):
                element = int(line[i])

                # elements begin at 1 therfore we subtract 1 for obtaining its index
                cover_matrix[element-1, col_idx] = 1
    return cover_matrix, cost_vector


def load_scp_instance(file_path):
    row = 0
    start = False
    with open(file_path, 'r') as file:
        for idx, line in enumerate(file, start=-1):
            if line.isspace():
                continue

            line = line.lstrip().rstrip('\n').rstrip(' ').split(' ')

            # First line contains dimensions
            if idx == -1:
                # Because number of subsets is first in this format we need to reverse 
                shape = tuple(int(x) for x in line)
                cover_matrix = np.zeros(shape, dtype=np.float16)
                cost_vector = []
            elif start and sets > 0:
                for col in line:
                    cover_matrix[row-1, int(col)-1] = 1
                sets -= len(line)
            elif len(line) == 1:
                row += 1
                sets = int(line[0])
                start = True
            else:
                cost_vector += list(map(float, line))
        cost_vector = np.array(cost_vector, dtype=np.float16)
            


    return cover_matrix, cost_vector



def assign_new_costs(file_name, cv):
    if file_name.startswith('rail'):
        orig_txt_path = 'instances/txt/Rail/' + file_name + '.txt'
        new_wcnf_path = 'instances/wcnf/Rail/' + file_name + "_" + str(cv).replace('.', '') + '.wcnf'
        new_txt_path = 'instances/txt/Rail/' + file_name + "_" + str(cv).replace('.', '') + '.txt'
        assign_new_costs_rail(orig_txt_path, new_txt_path, new_wcnf_path, cv)
    elif file_name.startswith('sts'):
        orig_txt_path = 'instances/txt/STS/' + file_name + '.txt'
        new_wcnf_path = 'instances/wcnf/STS/' + file_name + "_" + str(cv).replace('.', '') + '.wcnf'
        new_txt_path = 'instances/txt/STS/' + file_name + "_" + str(cv).replace('.', '') + '.txt'
        assign_new_costs_sts(orig_txt_path, new_txt_path, new_wcnf_path, cv)
    elif file_name.startswith('scpn'):
        orig_txt_path = 'instances/txt/OR-Large/' + file_name + '.txt'
        new_wcnf_path = 'instances/wcnf/OR-Large/' + file_name + "_" + str(cv).replace('.', '') + '.wcnf'
        new_txt_path = 'instances/txt/OR-Large/' + file_name + "_" + str(cv).replace('.', '') + '.txt'
        assign_new_costs_scp(orig_txt_path, new_txt_path, new_wcnf_path, cv)
    elif file_name.startswith('scpclr'):
        orig_txt_path = 'instances/txt/SCP-CLR/' + file_name + '.txt'
        new_wcnf_path = 'instances/wcnf/SCP-CLR/' + file_name + "_" + str(cv).replace('.', '') + '.wcnf'
        new_txt_path = 'instances/txt/SCP-CLR/' + file_name + "_" + str(cv).replace('.', '') + '.txt'
        assign_new_costs_scp(orig_txt_path, new_txt_path, new_wcnf_path, cv)
    elif file_name.startswith('scpcyc'):
        orig_txt_path = 'instances/txt/SCP-CYC/' + file_name + '.txt'
        new_wcnf_path = 'instances/wcnf/SCP-CYC/' + file_name + "_" + str(cv).replace('.', '') + '.wcnf'
        new_txt_path = 'instances/txt/SCP-CYC/' + file_name + "_" + str(cv).replace('.', '') + '.txt'
        assign_new_costs_scp(orig_txt_path, new_txt_path, new_wcnf_path, cv)
    elif file_name.startswith('scp'):
        orig_txt_path = 'instances/txt/OR-Small/' + file_name + '.txt'
        new_wcnf_path = 'instances/wcnf/OR-Small/' + file_name + "_" + str(cv).replace('.', '') + '.wcnf'
        new_txt_path = 'instances/txt/OR-Small/' + file_name + "_" + str(cv).replace('.', '') + '.txt'
        assign_new_costs_scp(orig_txt_path, new_txt_path, new_wcnf_path, cv)



def assign_new_costs_rail(orig_txt_path, new_txt_path, new_wcnf_path, cv):
    with open(orig_txt_path, 'r') as file:
        with open(new_txt_path, 'w') as new_file:
            for col_idx, line in enumerate(file, start=-1):
                line = line.lstrip().rstrip('\n').rstrip(' ').split(' ')

                # First line contains dimensions
                if col_idx == -1:
                    new_file.write(' ' + ' '.join(line) + ' \n')
                    shape = tuple(int(x) for x in line)
                    cost_vector = sample(cv, shape[1])
                    continue
                # First entry in row is cost of subset
                line[0] = str(cost_vector[col_idx])
                new_str = ' ' + ' '.join(line) + ' \n'
                new_file.write(new_str)
    encode_rail_instance(new_txt_path, new_wcnf_path)


def assign_new_costs_sts(orig_txt_path, new_txt_path, new_wcnf_path, cv):
    with open(orig_txt_path, 'r') as file:
        with open(new_txt_path, 'w') as new_file:
            for col_idx, line in enumerate(file, start=-1):
                if line.isspace():
                    continue


                line = line.lstrip().rstrip('\n').rstrip(' ').split(' ')
                line = [c for c in line if c != '']

                if col_idx == -1:
                    new_file.write(' ' + ' '.join(line) + ' \n')

                    shape = tuple(int(x) for x in line if x != '')
                    shape = tuple(int(x) for x in line)
                    cost_vector = sample(cv, shape[1])
                    continue

                if len(line) == 3:
                    line.append(str(cost_vector[col_idx]))
                else:
                    line[3] = str(cost_vector[col_idx])
                
                new_str = ' ' + ' '.join(line) + ' \n'
                new_file.write(new_str)
    encode_sts_instance(new_txt_path, new_wcnf_path)

def assign_new_costs_scp(orig_txt_path, new_txt_path, new_wcnf_path, cv):
    with open(orig_txt_path, 'r') as file:
        with open(new_txt_path, 'w') as new_file:
            start = False
            for idx, line in enumerate(file, start=-1):

                if line.isspace():
                    continue
                
                line = line.lstrip().rstrip('\n').rstrip(' ').split(' ')

                # First line contains dimensions
                if idx == -1:
                    new_file.write(' ' + ' '.join(line) + ' \n')

                    # Because number of subsets is first in this format we need to reverse 
                    shape = tuple(int(x) for x in line)
                    cost_vector = iter(sample(cv, shape[1]))
                elif start:
                    new_file.write(' ' + ' '.join(line) + ' \n')
                elif len(line) == 1:
                    start = True
                    # costs are specified right before subset elements
                    new_file.write(' ' + ' '.join(line) + ' \n')
                else:
                    new_file.write(' ')
                    for _ in line:
                        new_file.write(str(next(cost_vector)) + ' ')
                    new_file.write('\n')
    encode_scp_instance(new_txt_path, new_wcnf_path) 
                

                


