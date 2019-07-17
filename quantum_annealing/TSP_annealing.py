import numpy as np
import scipy.io
import random
import itertools
import math
from dwave_qbsolv import QBSolv
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import FixedEmbeddingComposite
import minorminer
import networkx as nx
import neal
from random_graph_generator import graphs_decipher
from tsp_dp_solver import get_distance_matrix


#read the dataset
n=6
target_file="random_graphs.csv"
graphs=graphs_decipher(target_file,n)
#20 TSPs

for g in graphs:
    distance_matrix=get_distance_matrix(g)
    node={}
    coupler_constraint_sum_i={}
    coupler_constraint_sum_s={}
    coupler_distance={}
    coupler_boundary={}
#qubits are encoded by q_{(i,a)}, i in 1,...,6 and a in 1,...,6
#penalty strength 100\sqrt{2}
    lamb=145
    mu=145
    for i in range (1,n+1):
        for s in range (1,n+1):
            node[(i,s),(i,s)]=-lamb-mu
#constraint condition \sum_i q_i,s=1
    for s in range (1,n+1):
        for i in range (1,n+1):
            for j in range (i+1,n+1):
                coupler_constraint_sum_i[(i,s),(j,s)]=2*lamb
#constraint condition \sum_s q_i,s=1
    for i in range (1,n+1):
        for s in range (1,n+1):
            for t in range(s+1,n+1):
                coupler_constraint_sum_s[(i,s),(i,t)]=2*mu
#for cost function
    for i in range (1,n+1):
        for j in range (1,n+1):
            for s in range (1,n):
                if i!=j:
                    coupler_distance[(i,s),(j,s+1)]=distance_matrix[i-1][j-1]
#for boundary into consideration
    for i in range (1,n+1):
        for j in range (1,n+1):
            if i!=j:
                coupler_boundary[(i,1),(j,n)]=distance_matrix[i-1][j-1]
                
#generate QUBO
    QUBO={}
    QUBO.update(node)
    QUBO.update(coupler_constraint_sum_i)
    QUBO.update(coupler_constraint_sum_s)
    QUBO.update(coupler_distance)
    QUBO.update(coupler_boundary)

# define (sub)problem size
#solver_limit = 40
#find embedding of subproblem-sized complete graph to the QPU
#G = nx.complete_graph(solver_limit)
#system = DWaveSampler()
#embedding = minorminer.find_embedding(G.edges, system.edgelist)
#response = QBSolv().sample_qubo(QUBO, solver=FixedEmbeddingComposite(system, embedding), solver_limit=solver_limit)




    response = QBSolv().sample_qubo(QUBO,num_repeats=50)


    result={}
    result.update(list(response.samples())[0])
#result_decode
    cost=0
    for i in range (1,n+1):
        for j in range (1,n+1):
            for s in range (1,n+1):
                if i!=j:
                    if s+1<7:
                        distance=distance_matrix[i-1][j-1]*result[(i,s)]*result[(j,s+1)]
                    else:
                        distance=distance_matrix[i-1][j-1]*result[(i,s)]*result[(j,1)]
                    cost=cost+distance
    print(cost)