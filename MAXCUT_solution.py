# -*- coding: utf-8 -*-
import pandas as pd
import networkx as nx


from optimizeq.utils.maxcut_solver import goemans_williamson
from optimizeq.utils import report
from optimizeq.utils.random_graph_generator import gen_adj_matr_list, decode_matrix_list
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', help="problem size", type=int)
parser.add_argument('-N', help="sample size", type=int)

args = parser.parse_args()

#%%
# set params

if args.N is None:
    N = 100
else:
    N = args.N

if args.n is None:
    n = 4
else:
    n = args.n

tag = "_n={}_N={}".format(n, N)

matrix_file = "./data/random_maxcut_matrix"+tag
solution_file = "./data/classical_maxcut_solution"+tag
#%%
# generate matrix
gen_adj_matr_list(matrix_file, N, n)

#%%

data = decode_matrix_list(matrix_file, n)

print("generating solutions...")

result = []
for i in range(len(data)):
    m = data[i]
    (conf, cost, bound) = goemans_williamson(nx.to_networkx_graph(m))
    result.append([conf, cost])
    report(i, N//10, N)

#%% save data using pandas

pd.DataFrame(result).to_csv(solution_file)
print("data saved to file!")
