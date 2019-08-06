# implement for a 2d numpy array, consider add support for networkx graph
import numpy as np
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


def TSP_Ansatz(distance_matrix):
    D = distance_matrix

    def H_ps(u, v, i, j):
        '''
        swap if reach city u at step i and reach city v and step j
        '''
        pass

# test for implementation
if __name__=="__main__":
#     # ===================================
    print(TSP_Hamiltonian(np.array([[ 0.        , 63.66447662, 64.03085272],
       [63.66447662,  0.        , 30.05756898],
       [64.03085272, 30.05756898,  0.        ]])))
