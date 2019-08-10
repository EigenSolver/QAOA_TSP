# -*- coding: utf-8 -*-


import pandas as pd

from lib.random_graph_generator import decode_matrix_list
from lib.graph_converter import MAXCUT_Hamiltonian
from lib.qaoa_simple import QAOA
from lib.utilities import timer, report

# %% initialize engine

from lib.projectq_header import * # eng is initialized!

print('compiler engine initialization...')

matrix_file="./data/random_maxcut_matrix.txt"
solution_file="./data/qaoa_maxcut_solution"



#%% set parameters

p=2
n=10
N=100
n_sampling=20
report_rate=2

data=decode_matrix_list(matrix_file,n)[:N]


opt_method="COBYLA"
tag="_n={0}_p={1}_method={2}".format(n,p,opt_method)

# %%
print("maxcut with "+tag)


solution=[]
for i in range(N):
    H_cost=MAXCUT_Hamiltonian(data[i])
    
    qaoa=QAOA(eng,H_cost,n,n_steps=p)
    qaoa.run(method=opt_method)
    
    param=qaoa.result.x
    evaluate_cost=qaoa.result.fun
    
    n_iter=qaoa.result.nfev
    conf, cost=qaoa.get_solution(draw=n_sampling)
    
    solution.append([param, conf, cost, evaluate_cost, n_iter])
    report(i,report_rate,N)
    
#%%
print("saving data...")
pd.DataFrame(solution,columns=["opt_param", "final_state", "cost", "mean_cost", "n_iteration"]).to_csv(solution_file+tag)

#%%





