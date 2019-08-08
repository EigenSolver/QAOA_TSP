'''
module to provide all the necessary ansatz and mixer setting to implement operator ansatz
'''

import numpy as np
from sympy import expand
from projectq.ops import QubitOperator, TimeEvolution
from projectq.ops import X

def complete_graph_edge_coloring_cluster(n):
    '''
    from Vizing's theorem in graph theory
    
    for a complete graph, the degree of each node is n-1
    there are n(n-1)/2 edges in the graph 
    
    if n is odd, there are n edge-coloring clusters, with (n-1)/2 edges in each cluster 
    if n is even, there are n-1 edge-coloring clusters, with n/2 edges in each cluster 
    
    give a complete graph with n vitices, return a cluster contains 
    
    Args:
        n(int): number of vertices in the graph
    Return:
        clusters(list): list of list(cluster) contains edges(tuple of 2-node) in the cluster
    >>> complete_graph_edge_coloring_cluster(5)
    [[(0, 1), (4, 2)], [(1, 2), (0, 3)], [(2, 3), (1, 4)], [(3, 4), (2, 0)], [(4, 0), (3, 1)]]
    >>> complete_graph_edge_coloring_cluster(6)
    [[(0, 1), (4, 2), (5, 3)], [(1, 2), (0, 3), (5, 4)], [(2, 3), (1, 4), (5, 0)], [(3, 4), (2, 0), (5, 1)], [(4, 0), (3, 1), (5, 2)]]
    '''

    clusters = []
    if n % 2 == 1:
        for i in range(n):
            edges = []
            for j in range((n-1)//2):
                edges.append(((i-j) % n, (i+1+j) % n))
            clusters.append(edges)
    elif n % 2 == 0:
        clusters = complete_graph_edge_coloring_cluster(n-1)
        for i in range(n-1):
            clusters[i].append((n-1, (i+n//2) % (n-1)))
    return clusters


def TSP_Ansatz(engine,n_qubits):
    '''
    Args:
        engine(MainEngine): engine to run simulator
        n_qubits(int): number of qubits, should be square for int
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

        for i in range(0,n-(n%2),2):
            for edge in pc:
                H+=H_partial_swap(edge[0],edge[1],i,i+1)
                
        H.compress()
        return H

    def H_even(pc):
        '''
        Args:
            pc(list): list of 2-tuple, represent edges in same color
        Return:
            H(QubitOperator): operator that add all the partial mixer with even steps and cities in same color
        '''

        H=0*QubitOperator("")
        for i in range(1,n+(n%2)-1,2):
            for edge in pc:
                H+=H_partial_swap(edge[0],edge[1],i,i+1)
        
        H.compress()
        return H

    def H_last(pc):
        '''

        '''
        H=0*QubitOperator("")
        for edge in pc:
            H+=H_partial_swap(edge[0],edge[1],n-1,0)
        H.compress()
        return H

    operators=[]
    colors=complete_graph_edge_coloring_cluster(n)
    for pc in colors:
        operators.append(H_last(pc))
        operators.append(H_even(pc))
        operators.append(H_odd(pc))
    return operators

if __name__=="__main__":
    from projectq_header import *
    from projectq.ops import All, Measure
    state=TSP_Ansatz(eng,16)

    eng.flush()
    All(Measure)|state
    print([int(x) for x in state])