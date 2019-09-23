# -*- coding: utf-8 -*-
import pandas as pd
from optimizeq.utils.random_graph_generator import decode_matrix_list
from optimizeq.hamiltonians import TSP_H_cost
from optimizeq.ansatzes import TSP_H_mixers, TSP_Ansatz
from optimizeq.utils.tsp_solver import tsp_cost, tsp_bits_convert
from optimizeq import QAOA
from optimizeq.utils import timer, report
from optimizeq.utils.projectq_header import *  # eng is initialized!
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', help="problem size", type=int)
parser.add_argument('-p', help="QAOA layer number", type=int)

args = parser.parse_args()

# %% initialize engine

print('compiler engine initialization...')

postfix = "_n=4_N=100"
matrix_file = "./data/random_tsp_matrix"+postfix
solution_file = "./data/qaoa_tsp_solution"


#%% set parameters
if args.p is None:
    p = 1
else:
    p = args.p

if args.n is None:
    n = 4
else:
    n = args.n

N = 100


n_qubits = (n-1)**2
report_rate = 1
n_sampling = 50

data = decode_matrix_list(matrix_file, n)
assert N <= len(data)
data = data[:N]


opt_method = "COBYLA"
opt_option = {'maxiter': 100, 'tol': 0.2}

tag = "_n={0}_N={1}_p={2}_method={3}".format(n, N, p, opt_method)

# %%
print("tsp with "+tag)


solution = []
with open(solution_file, "w") as f:  # write in time!
    for i in range(N):
        matr = data[i]
        H_cost = TSP_H_cost(matr)
        H_mixer = TSP_H_mixers(n-1)
        def cost_func(x): return tsp_cost(
            tsp_bits_convert(x, prepend=True), matr)
        qaoa = QAOA(eng, H_cost, n_qubits, n_steps=p, H_mixer=H_mixer, ansatz_func=TSP_Ansatz,
                    cost_eval=cost_func, verbose=True)  # apply operator ansatz

        # qaoa = QAOA(eng, H_cost, n_qubits, n_steps=p, n_sampling=0)  # naive version

        qaoa.run(method=opt_method, options=opt_option)

        param = qaoa.result.x
        evaluate_cost = qaoa.result.fun

        n_iter = qaoa.result.nfev
        conf, cost = qaoa.get_best_solution(draw=10)
        conf = tsp_bits_convert(conf, prepend=True)

        solution.append([param, conf, cost, evaluate_cost, n_iter])
        f.write(str(solution[-1])+"\n")
        report(i, report_rate, N)

#%%
print("saving data...")
pd.DataFrame(solution, columns=["opt_param", "final_state",
                                "cost", "mean_cost", "n_iteration"]).to_csv(solution_file+tag)

#%%
