
import numpy as np
import os
from pysat.formula import WCNF
from sample import sample









    # instance.encode_as_wcnf()

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
        elif file_name.startswith('rand'):
            self.txt_path = 'instances/txt/Rand/' + file_name + '.txt'
            self.wcnf_path = 'instances/wcnf/Rand/' + file_name + '.wcnf'
        
        self.file_name = file_name
        self.cover_matrix = None
        self.cost_vector = None

    

    def set_cover_matrix(self, cover_matrix):
        self.cover_matrix = cover_matrix

    def set_cost_vector(self, cost_vector):
        self.cost_vector = cost_vector

    def set_solver(self, solver):
        self.solver = solver

        
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
        subset_sizes = np.sum(self.cover_matrix, axis=0, dtype=np.uint8)

        # Get the number of columns
        num_elements = self.cover_matrix.shape[0]

        subset_size_ratios = subset_sizes / num_elements
        relative_set_cost = (self.cost_vector * np.mean(subset_size_ratios)) / np.mean(self.cost_vector) 
        subset_size_cost_ratio = subset_size_ratios / relative_set_cost 

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

    def cost_features(self):
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
    
    # def graph_features(self):
    #     adjacency_matrix = self.calc_graph()
    #     graph = nx.from_numpy_array(adjacency_matrix)

    #     nx.draw(graph, with_labels=True, node_color='lightblue', node_size=50, font_size=12, font_weight='bold', width=2)


    #     connected_components = list(nx.connected_components(graph))
    #     cycles = list(nx.simple_cycles(graph))
    #     shortest_cycle = min(cycles, key=len)
    #     longest_cycle = max(cycles, key=len)
        
    #     return \
    #     len(connected_components), \
    #     len(shortest_cycle), \
    #     len(longest_cycle)

    def load(self):
        row = 0
        start = False
        with open(self.txt_path, 'r') as file:
            for idx, line in enumerate(file, start=-1):
                if line.isspace():
                    continue

                line = line.lstrip().rstrip('\n').rstrip(' ').split(' ')

                # First line contains dimensions
                if idx == -1:
                    # Because number of subsets is first in this format we need to reverse 
                    shape = tuple(int(x) for x in line)
                    self.cover_matrix = np.zeros(shape, dtype=np.uint8)
                    self.cost_vector = np.zeros(shape[1], dtype=np.uint8)
                    offset = 0
                elif start and sets > 0:
                    for col in line:
                        self.cover_matrix[row-1, int(col)-1] = 1
                    sets -= len(line)
                elif len(line) == 1:
                    row += 1
                    sets = int(line[0])
                    start = True
                else:
                    new_costs = list(map(lambda x: np.minimum(x, 255), list(map(int, line))))
                    self.cost_vector[offset:offset + len(new_costs)] = new_costs
                    offset += len(new_costs)


    def encode_as_wcnf(self, txt_path=None, wcnf_path=None):
        if txt_path is None:
            txt_path = self.txt_path
        if wcnf_path is None:
            wcnf_path = self.wcnf_path


        with open(txt_path, 'r') as txt_file:
            # for scp dimensions are switched
            first_line = txt_file.readline().lstrip().rstrip('\n').rstrip(' ').split(' ')
            shape = tuple(int(x) for x in first_line)
            wcnf = WCNF()
            hard_clauses = [[] for _ in range(shape[0])]
            elem = 0
            cost_nr = 0
            start = False
            for _, line in enumerate(txt_file, start=1):

                if line.isspace():
                    continue

                line = line.lstrip().rstrip('\n').rstrip(' ').split(' ')

                if start and sets > 0:
                    for set_nr in line:
                        hard_clauses[elem-1].append(int(set_nr))
                    sets -= len(line)
                # costs are specified right before subset elements
                elif len(line) == 1:
                    elem += 1
                    sets = int(line[0])
                    start = True        
                else:
                    for e in line:
                        cost_nr += 1
                        wcnf.append([-1 * cost_nr], weight=int(e))

        # add hard clauses to make sure each element is covered
        wcnf.extend(hard_clauses)

        # export file and modify it to fit the format
        wcnf.to_file(fname=wcnf_path, compress_with='use_ext')
        with open(wcnf_path, 'r') as wcnf_file:
            hard_clause_indicator = wcnf_file.readline().lstrip().rstrip('\n').rstrip(' ').split(' ')[-1]
            command = f"sed -i 's/{hard_clause_indicator}/h/g' {wcnf_path}"
            os.system(command)
            os.system(f"gawk -i inplace 'NR>1' {wcnf_path}")         
    

    def assign_new_costs_cv(self, cv):
        new_txt_path = self.txt_path.replace(self.file_name, self.file_name + "_cv_" + str(cv).replace('.', ''))
        new_wcnf_path = new_txt_path.replace('txt', 'wcnf')
        with open(self.txt_path, 'r') as file:
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
                        new_file.write(' ' + ' '.join(line) + ' \n')
                    else:
                        new_file.write(' ')
                        for _ in line:
                            new_file.write(str(next(cost_vector)) + ' ')
                        new_file.write('\n')
        self.encode_as_wcnf(new_txt_path, new_wcnf_path) 

    
    def assign_new_costs_margin(self, factor):
        if 0 < factor or factor > 1:
            pass
        if self.cover_matrix is None:
            self.load()
        
        new_txt_path = self.txt_path.replace(self.file_name, self.file_name + "_scr_"+ str(factor).replace('.', ''))
        new_wcnf_path = new_txt_path.replace('txt', 'wcnf')
                
        cardinalities = np.sum(self.cover_matrix, axis=0)

        with open(self.txt_path, 'r') as file:
            with open(new_txt_path, 'w') as new_file:
                start = False
                for idx, line in enumerate(file, start=-1):

                    if line.isspace():
                        continue
                    
                    line = line.lstrip().rstrip('\n').rstrip(' ').split(' ')

                    # First line contains dimensions
                    if idx == -1:
                        new_file.write(' ' + ' '.join(line) + ' \n')
                        cost_vector = iter([np.random.randint(max(1, int(e - e * factor)), int(e + e * factor) + 1) for e in cardinalities])
                    elif start:
                        new_file.write(' ' + ' '.join(line) + ' \n')
                    elif len(line) == 1:
                        start = True
                        new_file.write(' ' + ' '.join(line) + ' \n')
                    else:
                        new_file.write(' ')
                        for _ in line:
                            new_file.write(str(next(cost_vector)) + ' ')
                        new_file.write('\n')
        self.encode_as_wcnf(new_txt_path, new_wcnf_path) 

                


