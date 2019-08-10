# -*- coding: utf-8 -*-
# implement for a 2d numpy array, consider add support for networkx graph
import numpy as np
from sympy import expand
from projectq.ops import QubitOperator, TimeEvolution
from lib.graph_converter import complete_graph_edge_coloring_cluster
from projectq.ops import X

def TSP_H_mixers(n):
    '''
    Args:
        n(int): size of problem
    Return:
        operators(list): list of unitary operators
    '''
    index= lambda u,i: i*n+u  

    def H_swap(u, v, i, j):
        '''
        give four index where u,v denote cities in graph, and i,j denote step in tour
        return swap Hamiltonian that swap the order of u and v, if u at i and j at v

        Here we use Mathematica to expand the operator to X,Y gate composition 
        and implement this formula in raw code

        Args:
            u,v(int): label of cities
            i,j(int): label of steps
        Return:
            H_s(QubitOperator): four-bit operator, swap Hamiltonian
        '''

        add_label=lambda x: x.format(index(u, i), index(v, j), index(u, j), index(v, i))
        term_list=\
        '''- 1.0j, X{0} X{1} X{2} Y{3} 
        - 1.0j, X{0} X{1} X{3} Y{2} 
        + 1.0j, X{0} X{2} X{3} Y{1} 
        - 1.0j, X{0} Y{1} Y{2} Y{3} 
        + 1.0j, X{1} X{2} X{3} Y{0} 
        - 1.0j, X{1} Y{0} Y{2} Y{3} 
        + 1.0j, X{2} Y{0} Y{1} Y{3} 
        + 1.0j, X{3} Y{0} Y{1} Y{2} 
        + 1.0, X{0} X{1} X{2} X{3} 
        - 1.0, X{0} X{1} Y{2} Y{3} 
        + 1.0, X{0} X{2} Y{1} Y{3} 
        + 1.0, X{0} X{3} Y{1} Y{2} 
        + 1.0, X{1} X{2} Y{0} Y{3} 
        + 1.0, X{1} X{3} Y{0} Y{2} 
        - 1.0, X{2} X{3} Y{0} Y{1} 
        + 1.0, Y{0} Y{1} Y{2} Y{3}'''

        term_list = map(lambda x: x.split(","), term_list.split("\n"))
        
        H_s=0*QubitOperator("")
        for term in term_list:
            coeff=complex(term[0].replace(" ",""))
            operator=QubitOperator(add_label(term[1]))
            H_s+=coeff*operator

        return H_s

    def H_partial_swap(u, v, i, j):
        return H_swap(u, v, i, j)+H_swap(u, v, j, i) # does order matter here??

    def H_odd(pc):
        '''
        Args:
            pc(list): list of 2-tuple, represent edges in same color
        Return:
            H(QubitOperator): operator that add all the partial mixer with even steps and cities in same color

        '''
        H=0*QubitOperator("")
        if n%2:
            for i in range(0,n-1,2):
                for edge in pc:
                    H+=H_partial_swap(edge[0],edge[1],i,i+1)
        else:
            for i in range(0,n,2):
                for edge in pc:
                    H+=H_partial_swap(edge[0],edge[1],i,i+1)
        return H

    def H_even(pc):
        '''
        Args:
            pc(list): list of 2-tuple, represent edges in same color
        Return:
            H(QubitOperator): operator that add all the partial mixer with even steps and cities in same color
        '''

        H=0*QubitOperator("")
        for i in range(1,n,2):
            for edge in pc:
                H+=H_partial_swap(edge[0],edge[1],i,i+1)
        return H

    def H_last(pc):
        '''

        '''
        if n%2:
            for edge in pc:
                H=H_partial_swap(edge[0],edge[1],n-1,0)
            return H
        else:
            return 1*QubitOperator("")

    operators=[]
    colors=complete_graph_edge_coloring_cluster(n)
    for pc in colors:
        operators.append(H_last(pc))
        operators.append(H_even(pc))
        operators.append(H_odd(pc))
    return operators


def TSP_Ansatz(engine,n_qubits):
    '''
    Args:
        engine(MainEngine): engine to run simulator
        n_qubits(int): number of qubits
    Return:
        ansatz(Qureg): quantum register with diagnoal setting as ansatz of TSP
    '''
    assert np.sqrt(n_qubits)%1==0
    n=int(np.sqrt(n_qubits))
    index = lambda u,i: i*n+u  

    ansatz=engine.allocate_qureg(n_qubits)
    for i in range(n):
        X|ansatz[index(i,i)]
    
    return ansatz



# if __name__=="__main__":
#     n=3
#     # print(H_swap(1,3,4,5))
#     # print(H_partial_swap(1,3,4,5))
#     from lib.projectq_header import *
#     from projectq.ops import X, All, Measure,TimeEvolution
#     state=eng.allocate_qureg(16)

#     n=4
#     X|state[index(0,0)]
#     X|state[index(3,1)]
#     X|state[index(1,2)]
#     X|state[index(2,3)]

#     H_partial_swap(3,1,1,2)|state
#     All(Measure) | state
#     eng.flush()

#     print([int(x) for x in state])