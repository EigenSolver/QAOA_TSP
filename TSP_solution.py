# -*- coding: utf-8 -*-
import pandas as pd
from lib.tsp_solver import held_karp
from lib.utilities import report
from lib.random_graph_generator import gen_dist_matr_list, decode_matrix_list

#%%
# set params
matrix_file = "./data/random_tsp_matrix.txt"
solution_file = "./data/classical_tsp_solution.txt"

N = 100
n = 5
scale=10
tag = "_n={}_N={}".format(n,N)

#%%
# generate matrix
gen_dist_matr_list(matrix_file,N,n,scale)

#%%

data = decode_matrix_list(matrix_file,n)

print("generating solutions...")

result=[]
for i in range(len(data)):
    m=data[i]
    (cost, conf)= held_karp(m)
    result.append([conf,cost])
    report(i,n,N)

#%% save data using pandas

pd.DataFrame(result).to_csv(solution_file)
print("data saved to file!")