# implement for a 2d numpy array, consider add support for networkx graph
import projectq as pq
from projectq import MainEngine
from projectq.ops import All, Measure, QubitOperator, TimeEvolution, X, H

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar

def graph_to_hamiltonian(distance_matrix,weight_matrix=None,penalty_coeff=None):
    '''
    parameters
        distance_matrix: (2d numpy array)
        weight_matrix: (2d numpy array)
        penalty_coeff: (1d numpy array len 2n) coefficient for penalty hamiltonian
    return 
        H_tsp: (QubitOperator) Hamiltonian for TSP
    '''

    W=weight_matrix or np.ones(distance_matrix.shape)
    D=distance_matrix
    n=distance_matrix.shape[0]
    penalty_coeff=penalty_coeff or np.ones(2*n)
    param_mu=penalty_coeff[:n]
    param_lambd=penalty_coeff[n:]
    
    
    def H_cross(i,j):
        H_cross=QubitOperator("Z{0} Z{1}".format(i,j))+QubitOperator("Z"+str(i))\
        +QubitOperator("Z"+str(j))+QubitOperator(" ")
        return 1/4*H_cross
    
    def index(i,j):
        return i*n+j
    
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
if __name__=="__main__":
    from classical_TSP.random_graph_generator import gen_graph
    from classical_TSP.tsp_dp_solver import get_distance_matrix   
    n=6
    g=gen_graph(n)
    distance_matrix=get_distance_matrix(g)

    print(graph_to_hamiltonian(distance_matrix))