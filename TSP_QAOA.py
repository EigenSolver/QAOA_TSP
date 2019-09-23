# -*- coding: utf-8 -*-
import pandas as pd
from optimizeq.utils.random_graph_generator import decode_matrix_list
from optimizeq.hamiltonians import TSP_H_cost
from optimizeq.ansatzes import TSP_H_mixers, TSP_Ansatz
from optimizeq.utils.tsp_solver import tsp_cost, tsp_bits_convert
from optimizeq import QAOA
from optimizeq.utils import timer, report
from optimizeq.utils.projectq_header import *  # eng is initialized!
from optimizeq.utils import qaoa_arg_parser

args = qaoa_arg_parser.parse_args()
N = args.N
n = args.n
p = args.p

# %% initialize engine

print('compiler engine initialization...')

tag = "_n={}_N={}".format(n, N)
matrix_file = "./data/random_tsp_matrix"+tag
solution_file = "./data/qaoa_tsp_solution"


#%% set parameters

n_qubits = (n-1)**2
report_rate = 1
n_sampling = 20

data = decode_matrix_list(matrix_file, n)
assert N <= len(data)
data = data[:N]


opt_method = "COBYLA"
opt_option = {'maxiter': 10000, 'tol': 0.2}

tag = "_n={0}_N={1}_p={2}_method={3}".format(n, N, p, opt_method)

# %%
print("tsp with "+tag)


solution = []
with open(solution_file, "w") as f:  # write in time!
    for i in range(N):
        matr = data[i]
        H_cost = TSP_H_cost(matr)
        H_mixer = TSP_H_mixers(n-1)
        # print(TSP_Ansatz(eng,n_qubits))
        def cost_func(x): return tsp_cost(
            tsp_bits_convert(x, prepend=True), matr)
        qaoa = QAOA(eng, H_cost, n_qubits, n_steps=p, H_mixer=H_mixer, ansatz_func=TSP_Ansatz,
                    cost_eval=cost_func, verbose=True)  # apply operator ansatz

        # qaoa = QAOA(eng, H_cost, n_qubits, n_steps=p, n_sampling=0)  # naive version

        qaoa.run(method=opt_method, options=opt_option)

        param = qaoa.result.x
        evaluate_cost = qaoa.result.fun

        n_iter = qaoa.result.nfev
        conf, cost = qaoa.get_best_solution(draw=n_sampling)
        conf = tsp_bits_convert(conf, prepend=True)

        solution.append([param, conf, cost, evaluate_cost, n_iter])
        f.write(str(solution[-1])+"\n")
        report(i, report_rate, N)

#%%
print("saving data...")
pd.DataFrame(solution, columns=["opt_param", "final_state",
                                "cost", "mean_cost", "n_iteration"]).to_csv(solution_file+tag)

#%%
