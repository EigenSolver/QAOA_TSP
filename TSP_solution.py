# -*- coding: utf-8 -*-
import pandas as pd
from optimizeq.utils.tsp_solver import held_karp
from optimizeq.utils import report
from optimizeq.utils.random_graph_generator import gen_dist_matr_list, decode_matrix_list

#%%
# set params
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', help="problem size", type=int)
parser.add_argument('-N', help="sample size", type=int)

args = parser.parse_args()

if args.N is None:
    N = 100
else:
    N = args.N

if args.n is None:
    n = 4
else:
    n = args.n


scale = 10
tag = "_n={}_N={}".format(n, N)

matrix_file = "./data/random_tsp_matrix"+tag
solution_file = "./data/classical_tsp_solution"+tag
#%%
# generate matrix
gen_dist_matr_list(matrix_file, N, n, scale)

#%%

data = decode_matrix_list(matrix_file, n)

print("generating solutions...")

result = []
for i in range(len(data)):
    m = data[i]
    (cost, conf) = held_karp(m)
    result.append([conf, cost])
    report(i, n, N)

#%% save data using pandas

pd.DataFrame(result).to_csv(solution_file)
print("data saved to file!")
