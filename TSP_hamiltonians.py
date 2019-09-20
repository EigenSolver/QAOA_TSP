# -*- coding: utf-8 -*-
import pandas as pd

from qaoa.tests.random_graph_generator import decode_matrix_list
from qaoa.hamiltonians.graph_converter import TSP_H_cost
from qaoa.ansatzes.operator_ansatz import TSP_H_mixers, TSP_Ansatz
from qaoa.tests.tsp_solver import tsp_cost, tsp_bits_convert
from qaoa.backends.qaoa import QAOA
from qaoa.utils.utilities import timer, report

from qaoa.utils.projectq_header import *  # eng is initialized!

postfix = "_n=4_N=100"
matrix_file = "./data/random_tsp_matrix"+postfix
solution_file = "./data/qaoa_tsp_solution"

p = 1
n = 4
n_qubits = (n-1)**2
N = 1
report_rate = 1
n_sampling = 50

data = decode_matrix_list(matrix_file, n)
assert N <= len(data)
data = data[:N]

tag = "_n={0}_N={1}_p={2}".format(n, N, p)

# %%
print("TSP hamiltonians: "+tag)
matr = data[0]
H_mixer = TSP_H_mixers(n-1)
H_cost = TSP_H_cost(matr)
print("TSP Mixer:")
print(H_mixer)

with open("TSP_mixer.txt", 'w') as f:
    for h in H_mixer:
        f.write(h.__str__()+'\n\n')

print("TSP Cost:")
print(H_cost)
with open("TSP_cost.txt", 'w') as f:
    f.write(H_cost.__str__())
