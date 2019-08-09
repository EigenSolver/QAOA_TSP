# -*- coding: utf-8 -*-
import pandas as pd
import networkx as nx
from lib.maxcut_solver import goemans_williamson
from lib.utilities import report
from lib.random_graph_generator import gen_adj_matr_list, decode_matrix_list

#%%
# set params
matrix_file = "./data/random_maxcut_matrix"
solution_file = "./data/classical_maxcut_solution"

N = 500
n = 10
tag = "_n={}_N={}".format(n,N)

#%%
# generate matrix
gen_adj_matr_list(matrix_file,N,n)

#%%

data = decode_matrix_list(matrix_file,n)

print("generating solutions...")

result=[]
for i in range(len(data)):
    m=data[i]
    (conf, cost, bound)= goemans_williamson(nx.to_networkx_graph(m))
    result.append([conf,cost])
    report(i,n,N)

#%% save data using pandas

pd.DataFrame(result).to_csv(solution_file)
print("data saved to file!")