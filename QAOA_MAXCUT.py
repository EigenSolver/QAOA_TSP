# -*- coding: utf-8 -*-


import pandas as pd

from lib.random_graph_generator import decode_matrix_list
from lib.graph_converter import MAXCUT_H_cost
from lib.qaoa_simple import QAOA
from lib.utilities import timer, report

# %% initialize engine

from lib.projectq_header import * # eng is initialized!

print('compiler engine initialization...')

matrix_file="./data/random_maxcut_matrix"
solution_file="./data/qaoa_maxcut_solution"



#%% set parameters

p=2
n=10
N=100
n_sampling=20
report_rate=2

data=decode_matrix_list(matrix_file,n)
assert N<=len(data)
data=data[:N]


opt_method="COBYLA"
opt_option={'maxiter': 100, 'tol': 0.1}
tag="_n={0}_N={1}_p={2}_method={3}".format(n,N,p,opt_method)


# %%
print("maxcut with "+tag)


solution=[]
for i in range(N):
    H_cost=MAXCUT_H_cost(data[i])
    
    qaoa=QAOA(eng,H_cost,n,n_steps=p)
    qaoa.run(method=opt_method,options=opt_option)
    
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





