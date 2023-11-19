from pathlib import Path
import sys
import os


def generate_instances(sizes, p_values):
    for instance_size in sizes:
        num_elems, num_sets = instance_size
        for i in range(4):
            p = p_values[i]
            file_name = f"rand_{num_elems}_{num_sets}_{str(p).replace('.','')}"
            txt_path = "instances/txt/Rand/" + file_name + ".txt"
            wcnf_path = "instances/wcnf/Rand/" + file_name + ".wcnf"
            generator_path = "utils/generate"
            os.system(f"{generator_path} {num_elems} {num_sets} {p} {txt_path} {wcnf_path}")





if __name__ == '__main__':
    sizes = [
        (500, 200),
        (5000, 1000),
        (25000, 10000),
        (50000, 25000),
        
        (200, 500),
        (1000, 5000),
        (10000, 25000),
        (25000, 50000),

        (250,   250),
        (5000,  5000),
        (10000, 10000),
        (35000, 35000)
    ]
    p_values = [0.2, 0.4, 0.6, 0.8]
    generate_instances(sizes, p_values)