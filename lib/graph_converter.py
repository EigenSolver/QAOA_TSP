# implement for a 2d numpy array, consider add support for networkx graph
import projectq as pq
from projectq import MainEngine
from projectq.ops import All, Measure, QubitOperator, TimeEvolution, X, H

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar


def MAXCUT_Hamiltonian(adjancent_matrix,minimum=True):
    '''
    parameters
        adjancent_matrix: (2d numpy array)
    return 
        H_cost: (QubitOperator) Hamiltonian for maxcut problem
    '''
    m=adjancent_matrix
    n=m.shape[0]

    H_cost=0*QubitOperator("")
    for i in range(n-1):
        for j in range(i+1,n):
            H_cost+=1/2*m[i,j]*(QubitOperator("Z{0} Z{1}".format(i,j))-QubitOperator(""))

    if minimum:
        return H_cost
    else:
        return (-1)*H_cost

def TSP_hamiltonian(distance_matrix,weight_matrix=None,penalty_coeff=None):
    '''
    parameters
        distance_matrix: (2d numpy array)
        weight_matrix: (2d numpy array)
        penalty_coeff: (1d numpy array len 2n) coefficient for penalty hamiltonian
    return 
        H_tsp: (QubitOperator) Hamiltonian for travelling salesman problem
    '''

    W=weight_matrix or np.ones(distance_matrix.shape)
    D=distance_matrix
    n=distance_matrix.shape[0]
    if penalty_coeff is None:
        penalty_coeff=np.ones(2*n)
    param_mu=penalty_coeff[:n]
    param_lambd=penalty_coeff[n:]
    
    
    def H_cross(i,j):
        H_cross=QubitOperator("Z{0} Z{1}".format(i,j))+QubitOperator("Z"+str(i))\
        +QubitOperator("Z"+str(j))+QubitOperator(" ")
        return 1/4*H_cross
    
    def index(i,j):
        return i*n+j
    
    # how to reduce the cost?
    H_cost=0*QubitOperator("")
    for s in range(n-1):
        for i in range(n):
            for j in range(n):
                H_cost+=D[i,j]*W[i,j]*H_cross(index(i,s),index(j,s+1))
    for i in range(n):
        for j in range(n):
            H_cost+=D[i,j]*W[i,j]*H_cross(index(i,0),index(j,n-1))
    
    def H_square(s,transpose=False):
        H_square=0*QubitOperator("")
        if not transpose:
            for i in range(n):
                for j in range(n):
                    if i!=j:
                        H_square+=H_cross(index(i,s),index(j,s))
                    else:
                        H_square+=2*(QubitOperator("Z"+str(i))+QubitOperator(""))
                    
                H_square-=QubitOperator("")+QubitOperator("Z"+str(index(i,s)))
        else:
            for i in range(n):
                for j in range(n):
                    if i!=j:
                        H_square+=H_cross(index(s,i),index(s,j))
                    else:
                        H_square+=2*(QubitOperator("Z"+str(i))+QubitOperator(""))
                H_square-=QubitOperator("")+QubitOperator("Z"+str(index(s,i)))
        
        H_square+=QubitOperator("")
        return H_square
    
    H_penalty=0*QubitOperator("")
    for s in range(n):
        H_penalty+=param_mu[s]*H_square(s)
        H_penalty+=param_lambd[s]*H_square(s,transpose=True)
    
    return H_cost+H_penalty
    
# test for implementation
# if __name__=="__main__":
#     # ===================================
#     from classical_algorithm.tsp_dp_solver import get_distance_matrix   
#     from classical_algorithm.random_graph_generator import gen_graph, gen_random_adjancent_matrix
#     n=6
#     g=gen_graph(n)
#     distance_matrix=get_distance_matrix(g)

#     # print(TSP_hamiltonian(distance_matrix))
#     # ====================
#     print("Maxcut Hamiltonian")
#     print(MAXCUT_Hamiltonian(gen_random_adjancent_matrix(3,threshold=1)))

#     # ======================
    
#     def default_mixer(n_qubits=3):
#         # generate mixer Hamiltonian
#         H_mixer = 0*QubitOperator("")
#         for i in range(n_qubits):
#             H_mixer += QubitOperator("X{}".format(i))
#         return H_mixer

#     print("Mixer Hamiltonian")
#     print(default_mixer())