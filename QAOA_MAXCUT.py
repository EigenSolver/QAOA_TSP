# -*- coding: utf-8 -*-

import projectq as pq
from projectq import MainEngine
from projectq.ops import QubitOperator, Measure, All, H, TimeEvolution
from projectq.meta import Loop
from lib.graph_converter import MAXCUT_Hamiltonian

import numpy as np
import scipy as sp

from lib.qaoa_simple import QAOA

def maxcut_solver(data_file,solution_file,p,report_rate=10,method="TNC"):
    data=np.loadtxt(data_file)
    N=data.shape[0]
    n=int(np.sqrt(data.shape[1]))
    tag="_n={0}_p={1}".format(n,p)
    print("maxcut with "+tag)
    global eng

    with open(solution_file+tag,'w') as f:
        for i in range(N):
            H_cost=MAXCUT_Hamiltonian(data[i,:].reshape((n,n)))
            qaoa=QAOA(eng,H_cost,n,n_steps=p)
            qaoa.optimize(method=method)
            f.write(str(qaoa.get_result().fun)+str(' '))
            f.write(str(qaoa.get_solution()))
            f.write('\n')
            if (i+1)%report_rate==0:
                print("progress {0}/{1}".format(i+1,N))

if __name__ == "__main__":
    from lib.hiq_header import *
    print('compiler engine initialization...')

    data_file="./data/random_adjancent_matrix.txt"
    solution_file="./data/maxcut_solution"
    
    for p in range(2,5):
        maxcut_solver(data_file,solution_file,p)
