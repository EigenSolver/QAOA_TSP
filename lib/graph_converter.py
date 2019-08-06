# implement for a 2d numpy array, consider add support for networkx graph
import numpy as np
from sympy import expand
from projectq.ops import QubitOperator


def MAXCUT_Hamiltonian(adjancent_matrix, minimum=True):
    '''
    parameters
        adjancent_matrix: (2d numpy array)
    return 
        H_cost: (QubitOperator) Hamiltonian for maxcut problem
    '''
    m = adjancent_matrix
    n = m.shape[0]

    H_cost = 0*QubitOperator("")
    for i in range(n-1):
        for j in range(i+1, n):
            H_cost += 1/2 * \
                m[i, j] * \
                (QubitOperator("Z{0} Z{1}".format(i, j))-QubitOperator(""))

    if minimum:
        return H_cost
    else:
        return (-1)*H_cost


def Naive_TSP_Hamiltonian(distance_matrix, weight_matrix=None, penalty_coeff=None):
    '''
    parameters
        distance_matrix: (2d numpy array)
        weight_matrix: (2d numpy array)
        penalty_coeff: (1d numpy array len 2n) coefficient for penalty hamiltonian
    return 
        H_tsp: (QubitOperator) Hamiltonian for travelling salesman problem
    '''

    W = weight_matrix or np.ones(distance_matrix.shape)
    D = distance_matrix
    n = distance_matrix.shape[0]
    if penalty_coeff is None:
        penalty_coeff = np.ones(2*n)
    param_mu = penalty_coeff[:n]
    param_lambd = penalty_coeff[n:]

    def H_cross(i, j):
        H_cross = QubitOperator("Z{0} Z{1}".format(i, j))+QubitOperator("Z"+str(i))\
            + QubitOperator("Z"+str(j))+QubitOperator(" ")
        return 1/4*H_cross

    def index(i, j):
        return i*n+j

    # how to reduce the cost?
    H_cost = 0*QubitOperator("")
    for s in range(n-1):
        for i in range(n):
            for j in range(n):
                H_cost += D[i, j]*W[i, j]*H_cross(index(i, s), index(j, s+1))
    for i in range(n):
        for j in range(n):
            H_cost += D[i, j]*W[i, j]*H_cross(index(i, 0), index(j, n-1))

    def H_square(s, transpose=False):
        H_square = 0*QubitOperator("")
        if not transpose:
            for i in range(n):
                for j in range(n):
                    if i != j:
                        H_square += H_cross(index(i, s), index(j, s))
                    else:
                        H_square += 2 * \
                            (QubitOperator("Z"+str(i))+QubitOperator(""))

                H_square -= QubitOperator("") + \
                    QubitOperator("Z"+str(index(i, s)))
        else:
            for i in range(n):
                for j in range(n):
                    if i != j:
                        H_square += H_cross(index(s, i), index(s, j))
                    else:
                        H_square += 2 * \
                            (QubitOperator("Z"+str(i))+QubitOperator(""))
                H_square -= QubitOperator("") + \
                    QubitOperator("Z"+str(index(s, i)))

        H_square += QubitOperator("")
        return H_square

    H_penalty = 0*QubitOperator("")
    for s in range(n):
        H_penalty += param_mu[s]*H_square(s)
        H_penalty += param_lambd[s]*H_square(s, transpose=True)

    return H_cost+H_penalty


def TSP_Hamiltonian(distance_matrix):
    D = distance_matrix
    n = distance_matrix.shape[0]

    def index(u, i):
        '''
        i: step
        u: city
        '''
        return i*n+u

    def H_cross(i, j):
        H_cross = QubitOperator("Z{0} Z{1}".format(i, j))
        return H_cross

    H_cost = 0*QubitOperator("")
    for i in range(n-1):
        for u in range(n):
            for v in range(n):
                H_cost += D[u, v]*H_cross(index(u, i), index(v, i+1))

    for u in range(n):
        for v in range(n):
            H_cost += D[u, v]*H_cross(index(u, 0), index(v, n-1))

    return H_cost



    def H_ps(u, v, i, j):
        '''
        swap if reach city u at step i and reach city v and step j
        '''
        S_p(u,i)S_p()

def TSP_Ansatz(distance_matrix):
    D = distance_matrix
    n = distance_matrix.shape[0]

    def index(u, i):
        '''
        args i: step u: city
        return index of i, u
        '''
        return i*n+u
    
    def S_p(u,i):
        return QubitOperator("X{}".format(index(u, i)))+1j*QubitOperator("Y{}".format(index(u, i)))

    def S_m(u,i):
        return QubitOperator("X{}".format(index(u, i)))-1j*QubitOperator("Y{}".format(index(u, i)))


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


# test for implementation
if __name__=="__main__":
    import doctest
    doctest.testmod()
