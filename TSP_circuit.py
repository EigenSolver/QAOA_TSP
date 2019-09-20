# -*- coding: utf-8 -*-
from qaoa.tests.random_graph_generator import decode_matrix_list
from qaoa.hamiltonians.graph_converter import TSP_H_cost
from qaoa.ansatzes.operator_ansatz import TSP_H_mixers, TSP_Ansatz
from qaoa.tests.tsp_solver import tsp_cost, tsp_bits_convert
from qaoa.backends.qaoa import QAOA
from projectq.ops import X, Y, Z, Rx, Ry, Rz, H, TimeEvolution, All, Measure, QubitOperator, CNOT, Swap
from projectq.backends import Simulator, CommandPrinter, ResourceCounter
from projectq.setups.restrictedgateset import get_engine_list
from projectq import MainEngine

engine_list = get_engine_list(
    one_qubit_gates=(X, Y, Z, Rx, Ry, Rz, H), two_qubit_gates=(CNOT,))
eng = MainEngine(CommandPrinter(accept_input=False), engine_list)


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

# %%
matr = data[0]
H_mixer = TSP_H_mixers(n-1)
H_cost = TSP_H_cost(matr)
main = QAOA(eng, H_cost, n_qubits, n_steps=p, H_mixer=H_mixer,
            ansatz_func=TSP_Ansatz)  # apply operator ansatz

state = main.prep_state([1, 2])
All(Measure) | state

#%%
