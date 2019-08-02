#!/usr/bin/env python
# coding: utf-8

# In[1]:


import projectq as pq
from projectq import MainEngine
from projectq.ops import QubitOperator, Measure, All, H, TimeEvolution
from projectq.meta import Loop
from lib.graph_converter import TSP_Hamiltonian
import numpy as np
import pandas as pd

from lib.qaoa_simple import QAOA
from lib.random_graph_generator import graphs_decipher, get_distance_matrix



# In[ ]:


if __name__ == "__main__":
    from lib.projectq_header import *
    print('compiler engine initialization...')

    data_file="./data/random_graphs.txt"
    solution_file="./data/tsp_solution"
    
    graphs=graphs_decipher(data_file,n)
    N=len(graphs)
    tag="n={0}_p={1}".format(n,p)
    print("TSP with "+tag)
    
    H_cost=TSP_Hamiltonian(get_distance_matrix(graphs[i]),penalty_coeff=penalty*np.ones(2*n))
    qaoa=QAOA(eng,H_cost,n**2,n_steps=p)
    qaoa.optimize(method=method)
    f.write(str(qaoa.get_result().fun)+str(' '))
    f.write(str(qaoa.get_solution()))
    f.write('\n')
    if (i+1)%report_rate==0:
        print("progress {0}/{1}".format(i+1,N))

