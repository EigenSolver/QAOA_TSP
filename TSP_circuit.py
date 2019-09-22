# -*- coding: utf-8 -*-
import os
import sys
from optimizeq.utils.random_graph_generator import decode_matrix_list
from optimizeq.hamiltonians import TSP_H_cost
from optimizeq.ansatzes import TSP_H_mixers, TSP_Ansatz
from optimizeq.utils.tsp_solver import tsp_cost, tsp_bits_convert
from optimizeq.utils.random_graph_generator import gen_random_points, get_distance_matrix
from optimizeq import QAOA

from projectq.ops import X, Y, Z, Rx, Ry, Rz, H, TimeEvolution, All, Measure, QubitOperator, CNOT, Swap
from projectq.backends import Simulator, CommandPrinter, ResourceCounter
from projectq.setups.restrictedgateset import get_engine_list
from projectq import MainEngine

import numpy as np
from optimizeq.utils import report

engine_list = get_engine_list(
    one_qubit_gates=(X, Y, Z, Rx, Ry, Rz, H), two_qubit_gates=(CNOT,))
eng = MainEngine(CommandPrinter(accept_input=False), engine_list)
# %%


def print_tsp_circuit(eng, n, p):
    n_qubits = (n-1)**2
    ori_stdout = sys.stdout
    sys.stdout = open("TSP_circuit_n={0}_p={1}.txt".format(n, p), "w")
    matr = get_distance_matrix(gen_random_points(n))
    H_mixer = TSP_H_mixers(n-1)
    H_cost = TSP_H_cost(matr)
    main = QAOA(eng, H_cost, n_qubits, n_steps=p, H_mixer=H_mixer,
                ansatz_func=TSP_Ansatz)  # apply operator ansatz

    state = main.prep_state(np.random.rand(2*p))
    eng.flush(deallocate_qubits=True)
    sys.stdout = ori_stdout

#%%
os.chdir("./data/circuits")
#%%
for n in range(14, 15):
    for p in range(1, 2):
        print_tsp_circuit(eng, n, p)
        print("n=", n, "p=", p)
