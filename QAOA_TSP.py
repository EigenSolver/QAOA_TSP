# -*- coding: utf-8 -*-
import pandas as pd

from lib.random_graph_generator import decode_matrix_list
from lib.graph_converter import TSP_H_cost
from lib.operator_ansatz import TSP_H_mixers, TSP_Ansatz
from lib.tsp_solver import tsp_cost, tsp_bits_convert
from lib.qaoa_sandbox import QAOA
from lib.utilities import timer, report

# %% initialize engine

from lib.projectq_header import * # eng is initialized!

print('compiler engine initialization...')

matrix_file="./data/random_tsp_matrix_n=4_N=100.txt"
solution_file="./data/qaoa_tsp_solution_n=4_N=100.txt"



#%% set parameters

p=1
n=4
n_qubits=n**2
N=100
report_rate=1
n_sampling=10
data=decode_matrix_list(matrix_file,n)[:N]


opt_method="COBYLA"
opt_option={'maxiter': 100}
tag="_n={0}_p={1}_method={2}".format(n,p,opt_method)

# %%
print("tsp with "+tag)


solution=[]
for i in range(N):
    matr=data[i]
    H_cost=TSP_H_cost(matr)
    H_mixer=TSP_H_mixers(n)
    cost_func=lambda x: tsp_cost(tsp_bits_convert(x),matr)
    
    
    qaoa=QAOA(eng,H_cost,n_qubits,n_steps=p,H_mixer=H_mixer,ansatz_func=TSP_Ansatz,n_sampling=0,cost_eval=cost_func,verbose=True)# apply operator ansatz

    # qaoa=QAOA(eng,H_cost,n_qubits,n_steps=p) #naive version

    qaoa.run(method=opt_method,options=opt_option)
    
    param=qaoa.result.x
    evaluate_cost=qaoa.result.fun
    
    n_iter=qaoa.result.nfev
    conf, cost=qaoa.get_solution(draw=20)
    
    solution.append([param, conf, cost, evaluate_cost, n_iter])
    report(i,report_rate,N)
    
#%%
print("saving data...")
pd.DataFrame(solution,columns=["opt_param", "final_state", "cost", "mean_cost", "n_iteration"]).to_csv(solution_file+tag)

#%%

#def maxcut_qaoa_solver(data_file,solution_file,p,report_rate=10,method="TNC"):




