from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from instances.instance import Instance

def assign_costs_cv_all():
    for file_path in Path('instances/txt').rglob('*'):
        if file_path.is_file():
            file_name = str(file_path).split('/')[-1].replace('.txt', '')
            if not 'cv' in file_name and not 'scr' in file_name:
                print(file_name) 
                instance = Instance(file_name)
                instance.assign_new_costs_cv(0)
                instance.assign_new_costs_cv(0.2)
                instance.assign_new_costs_cv(0.4)
                instance.assign_new_costs_cv(0.6)
                instance.assign_new_costs_cv(0.8)
                instance.assign_new_costs_cv(0.99)





if __name__ == '__main__':
    assign_costs_cv_all()