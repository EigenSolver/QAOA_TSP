# -*- coding: utf-8 -*-
import pandas as pd
from optimizeq.utils.random_graph_generator import decode_matrix_list
from optimizeq.utils.maxcut_solver import maxcut_count
from optimizeq.hamiltonians import maxcut_h_cost
from optimizeq.utils import timer, report
from optimizeq import QAOA
from optimizeq.utils.projectq_header import *  # eng is initialized!
from optimizeq.utils import qaoa_arg_parser

args = qaoa_arg_parser.parse_args()
N = args.N
n = args.n
p = args.p

# %%
print('compiler engine initialization...')

tag = "_n={}_N={}".format(n, N)
matrix_file = "./data/random_maxcut_matrix"+tag
solution_file = "./data/qaoa_maxcut_solution"


#%% set parameters

n_sampling = 20
report_rate = 1

data = decode_matrix_list(matrix_file, n)
assert N <= len(data)
data = data[:N]


opt_method = "COBYLA"
opt_option = {'maxiter': 10000, 'tol': 0.2}
tag = "_n={0}_N={1}_p={2}_method={3}".format(n, N, p, opt_method)

# backend = SimulatorMPI(gate_fusion=True, num_local_qubits=n)
# eng = HiQMainEngine(backend, engines)

# %%
print("maxcut with "+tag)

solution = []
for i in range(N):
    matr = data[i]
    H_cost = maxcut_h_cost(matr)
    def cost_func(x): return -maxcut_count(x, matr)
    qaoa = QAOA(eng, H_cost, n, n_steps=p, cost_eval=cost_func)
    qaoa.run(method=opt_method, options=opt_option)

    param = qaoa.result.x
    evaluate_cost = qaoa.result.fun

    n_iter = qaoa.result.nfev
    conf, cost = qaoa.get_best_solution(draw=n_sampling)

    solution.append([param, conf, cost, evaluate_cost, n_iter])
    report(i, report_rate, N)

#%%
print("saving data...")
pd.DataFrame(solution, columns=["opt_param", "final_state",
                                "cost", "mean_cost", "n_iteration"]).to_csv(solution_file+tag)

#%%
