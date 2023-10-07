
import numpy as np




class Instance:

    def __init__(self, file_path):
        instance_type = file_path.split('/')[2]


        match instance_type:
            case 'rail':
                self.cover_matrix, self.cost_vector = load_rail_instance(file_path)
            case 'scp-clr' | 'scp-cyc':
                self.cover_matrix, self.cost_vector = load_scp_instance(file_path)
            case 'sts':
                self.cover_matrix, self.cost_vector = load_sts_instance(file_path)



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



 