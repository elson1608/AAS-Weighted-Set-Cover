from instances.instance import Instance
from solvers.cplex import CplexSolver
from solvers.gurobi import GurobiSolver
from solvers.nusc import NuSCSolver
from solvers.nuwls import NuWLSSolver
import concurrent.futures
import time
import pandas as pd
from IPython.display import display
from pathlib import Path



def solve_cplex(instance, time_limit):
    return CplexSolver().solve(instance=instance, time_limit=time_limit)

def solve_gurobi(instance, time_limit):
    return GurobiSolver().solve(instance=instance, time_limit=time_limit)

def solve_nusc(instance, time_limit):
    return NuSCSolver().solve(instance=instance, time_limit=time_limit)

def solve_nuwls(instance, time_limit):
    return NuWLSSolver().solve(instance=instance, time_limit=time_limit)

def get_subset_size_features(instance):
    return list(instance.subset_size_features())

def get_subset_size_cost_ratio_features(instance):
    return list(instance.subset_size_cost_ratio_features())

def get_num_of_appearances_features(instance):
    return list(instance.num_of_appearances_features())

def get_cost_features(instance):
    return list(instance.cost_features())

def get_forced_set_feature(instance):
    return [instance.forced_set_feature()]

def create_dataset(time_limit):
     column_names = [
          'instance name',
          'instance size', 
          'subset_size_mean', 
          'subset_size_sd',
          'subset_size_mad',
          'subset_size_min', 
          'subset_size_q1', 
          'subset_size_median', 
          'subset_size_q3',       
          'subset_size_max',
          'subset_size_cost_ratio_mean', 
          'subset_size_cost_ratio_sd',
          'subset_size_cost_ratio_mad',
          'subset_size_cost_ratio_min', 
          'subset_size_cost_ratio_q1', 
          'subset_size_cost_ratio_median', 
          'subset_size_cost_ratio_q3',       
          'subset_size_cost_ratio_max',
          'num_of_appearances_mean', 
          'num_of_appearances_sd',
          'num_of_appearances_mad',
          'num_of_appearances_min', 
          'num_of_appearances_q1', 
          'num_of_appearances_median', 
          'num_of_appearances_q3',       
          'num_of_appearances_max',
          'costs_cv',
          'costs_rel_mad',
          'costs_qcd',
          'forced_sets',
          # 'graph_connected_components',
          # 'graph_shortest_cycle',
          # 'graph_longest_cycle'
          'time_cplex',
          'cost_cplex',
          'time_gurobi',
          'cost_gurobi',
          'time_nusc',
          'cost_nusc',
          'time_nuwls',
          'cost_nuwls'
     ]
     
     instance_names = [str(file_path).split('/')[-1].replace('.txt', '') for file_path in Path('instances/txt').rglob('*') if file_path.is_file()]

     # Create an empty DataFrame with specified column names
     df = pd.DataFrame(columns=column_names, index=range(len(instance_names)))
     
     
     for idx, instance_name in enumerate(instance_names):
          print(instance_name)

          instance = Instance(instance_name)     
          instance.load()


          with concurrent.futures.ThreadPoolExecutor() as executor:
               cplex_future = executor.submit(solve_cplex, instance, time_limit)
               gurobi_future = executor.submit(solve_gurobi, instance, time_limit)
               nusc_future = executor.submit(solve_nusc, instance, time_limit)
               nuwls_future = executor.submit(solve_nuwls, instance, time_limit)

               # Wait for all tasks to complete
               concurrent.futures.wait([cplex_future, gurobi_future, nusc_future, nuwls_future])

               # Retrieve results
               cplex_benchmark = cplex_future.result()
               gurobi_benchmark = gurobi_future.result()
               nusc_benchmark = nusc_future.result()
               nuwls_benchmark = nuwls_future.result()
          with concurrent.futures.ThreadPoolExecutor() as executor:
               subset_size_features_future = executor.submit(get_subset_size_features, instance)
               subset_size_cost_ratio_features_future = executor.submit(get_subset_size_cost_ratio_features, instance)
               num_of_appearances_features_future = executor.submit(get_num_of_appearances_features, instance)
               cost_features_future = executor.submit(get_cost_features, instance)
               forced_set_feature_future = executor.submit(get_forced_set_feature, instance)

               # Wait for all tasks to complete
               concurrent.futures.wait([subset_size_features_future, subset_size_cost_ratio_features_future,
                                        num_of_appearances_features_future, cost_features_future, forced_set_feature_future])

               # Retrieve results
               subset_size_features_result = subset_size_features_future.result()
               subset_size_cost_ratio_features_result = subset_size_cost_ratio_features_future.result()
               num_of_appearances_features_result = num_of_appearances_features_future.result()
               cost_features_result = cost_features_future.result()
               forced_set_feature_result = forced_set_feature_future.result()

          row = [instance_name] + \
          [f"{instance.cover_matrix.shape[0]} x {instance.cover_matrix.shape[1]}"] + \
          subset_size_features_result + \
          subset_size_cost_ratio_features_result + \
          num_of_appearances_features_result + \
          cost_features_result + \
          forced_set_feature_result + \
          list(cplex_benchmark) + \
          list(gurobi_benchmark) + \
          list(nusc_benchmark) + \
          list(nuwls_benchmark)
          df.loc[idx] = row
     df.to_csv(f'dataset_{time_limit}.csv', index=False)




if __name__ == "__main__":
     time_limit = 10
     create_dataset(time_limit)

     