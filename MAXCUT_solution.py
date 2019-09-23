# -*- coding: utf-8 -*-
import pandas as pd
import networkx as nx
from optimizeq.utils.maxcut_solver import goemans_williamson
from optimizeq.utils import report
from optimizeq.utils.random_graph_generator import gen_adj_matr_list, decode_matrix_list
from optimizeq.utils import qaoa_arg_parser

args = qaoa_arg_parser.parse_args()
N = args.N
n = args.n
p = args.p

#%%
# set params


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
