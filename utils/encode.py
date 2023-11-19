from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from instances.instance import Instance

def encode_as_scp(file_path):
    new_path = file_path.replace('_', '')
    with open(file_path, 'r') as file:
        with open(new_path, 'w') as new_file:
            first_line = file.readline().lstrip().rstrip('\n').rstrip(' ').split(' ')
            first_line = [c for c in first_line if c != '']
            num_sets = int(first_line[1])
            new_file.write(' '.join(first_line) + '\n')
            costs = num_sets * '1 '
            costs = costs.rstrip() 
            new_file.write(costs + '\n')

            for line in file:
                line = '3\n' + line
                new_file.write(line)

def encode_all_as_wcnf():
    for file_path in Path('instances/txt').rglob('*'):
        if file_path.is_file():
            file_name = str(file_path).split('/')[-1].replace('.txt', '') 
            instance = Instance(file_name)
            instance.encode_as_wcnf()





if __name__ == '__main__':
    encode_all_as_wcnf()