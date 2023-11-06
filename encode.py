import sys
import os
from pysat.formula import WCNF


def encode_rail_instance(file_path, dest_path):
    with open(file_path, 'r') as txt_file:
        first_line = txt_file.readline().lstrip().rstrip('\n').rstrip(' ').split(' ')
        shape = tuple(int(x) for x in first_line)
        wcnf = WCNF()
        hard_clauses = [[] for _ in range(shape[0])]
        for set_nr, line in enumerate(txt_file, start=1):
            line = line.lstrip().rstrip('\n').rstrip(' ').split(' ')
            
            # first entry is cost second entry is number of elements covered hence
            # they are skipped
            for e in line[2:]:
                hard_clauses[int(e) - 1].append(set_nr)

            # add soft clauses for costs            
            wcnf.append([-1 * set_nr], weight=int(line[0]))
        
        # add hard clauses to make sure each element is covered
        wcnf.extend(hard_clauses)

        # export file and modify it to fit the format
        wcnf.to_file(fname=dest_path, compress_with='use_ext')
        with open(dest_path, 'r') as wcnf_file:
            hard_clause_indicator = wcnf_file.readline().lstrip().rstrip('\n').rstrip(' ').split(' ')[-1]
            command = f"sed -i 's/{hard_clause_indicator}/h/g' {dest_path}"
            os.system(command)
            os.system(f"gawk -i inplace 'NR>1' {dest_path}")

def encode_scp_instance(file_path, dest_path):
    with open(file_path, 'r') as txt_file:
        # for scp dimensions are switched
        first_line = txt_file.readline().lstrip().rstrip('\n').rstrip(' ').split(' ')
        first_line.reverse()
        shape = tuple(int(x) for x in first_line)
        wcnf = WCNF()
        hard_clauses = [[] for _ in range(shape[0])]
        set_nr = 0
        for _, line in enumerate(txt_file, start=1):
            line = line.lstrip().rstrip('\n').rstrip(' ').split(' ')
            if all(element == '1' for element in line) or len(''.join(line)) == 0:
                continue
            
            # costs are specified right before subset elements
            if len(line) == 1:        
                set_nr += 1
                wcnf.append([-1 * set_nr], weight=int(line[0]))
                continue
            
            for e in line:
                hard_clauses[int(e) - 1].append(set_nr)

        # add hard clauses to make sure each element is covered
        wcnf.extend(hard_clauses)

        # export file and modify it to fit the format
        wcnf.to_file(fname=dest_path, compress_with='use_ext')
        with open(dest_path, 'r') as wcnf_file:
            hard_clause_indicator = wcnf_file.readline().lstrip().rstrip('\n').rstrip(' ').split(' ')[-1]
            command = f"sed -i 's/{hard_clause_indicator}/h/g' {dest_path}"
            os.system(command)
            os.system(f"gawk -i inplace 'NR>1' {dest_path}")


def encode_sts_instance(file_path, dest_path):
    with open(file_path, 'r') as txt_file:
        first_line = txt_file.readline().lstrip().rstrip('\n').rstrip(' ').split(' ')
        shape = tuple(int(x) for x in first_line if x != '')
        wcnf = WCNF()
        hard_clauses = [[] for _ in range(shape[0])]
        for set_nr, line in enumerate(txt_file, start=1):
            line = line.lstrip().rstrip('\n').rstrip(' ').split(' ')
            line = [c for c in line if c != '']
            for e in line:
                hard_clauses[int(e) - 1].append(set_nr)

            # add soft clauses for costs            
            wcnf.append([-1 * set_nr], weight=1)

        # add hard clauses to make sure each element is covered
        wcnf.extend(hard_clauses)

        # export file and modify it to fit the format
        wcnf.to_file(fname=dest_path, compress_with='use_ext')
        with open(dest_path, 'r') as wcnf_file:
            hard_clause_indicator = wcnf_file.readline().lstrip().rstrip('\n').rstrip(' ').split(' ')[-1]
            os.system(f"sed -i 's/{hard_clause_indicator}/h/g' {dest_path}")
            os.system(f"gawk -i inplace 'NR>1' {dest_path}")


if __name__ == "__main__":
    txt_dir = sys.argv[1]

    for root, dirs, files in os.walk(txt_dir):
        for file in files:
            file_path = os.path.join(root, file)
            dest_path = file_path.replace('txt', 'wcnf')

            if file_path is None:
                print('No file path was provided')
                exit

            instance_type = file_path.split('/')[-2]

            if instance_type == 'Rail':
                print(f'encoding {file_path}')
                encode_rail_instance(file_path, dest_path)
                print(f'done')
            elif instance_type in ['SCP-CLR', 'SCP-CYC', 'OR-Large', 'OR-Small']:
                print(f'encoding {file_path}')
                encode_scp_instance(file_path, dest_path)
                print(f'done')
            elif instance_type == 'STS':
                print(f'encoding {file_path}')
                encode_sts_instance(file_path, dest_path)
                print(f'done')
            else:
                raise Exception('Invalid file path')



