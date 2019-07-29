from typing import Tuple

import cvxpy as cvx
import networkx as nx
import numpy as np

def goemans_williamson(graph: nx.Graph) -> Tuple[np.ndarray, float, float]:
    """
    The Goemans-Williamson algorithm for solving the maxcut problem.
    Ref:
        Goemans, M.X. and Williamson, D.P., 1995. Improved approximation
        algorithms for maximum cut and satisfiability problems using
        semidefinite programming. Journal of the ACM (JACM), 42(6), 1115-1145
    Returns:
        np.ndarray: Graph coloring (+/-1 for each node)
        float:      The GW score for this cut.
        float:      The GW bound from the SDP relaxation
    """
    # Kudos: Originally implementation by Nick Rubin, with refactoring and
    # cleanup by Jonathon Ward and Gavin E. Crooks
    laplacian = np.array(0.25 * nx.laplacian_matrix(graph).todense())

    # Setup and solve the GW semidefinite programming problem
    psd_mat = cvx.Variable(laplacian.shape, PSD=True)
    obj = cvx.Maximize(cvx.trace(laplacian * psd_mat))
    constraints = [cvx.diag(psd_mat) == 1]  # unit norm
    prob = cvx.Problem(obj, constraints)
    prob.solve(solver=cvx.CVXOPT)

    evals, evects = np.linalg.eigh(psd_mat.value)
    sdp_vectors = evects.T[evals > float(1.0E-6)].T

    # Bound from the SDP relaxation
    bound = np.trace(laplacian @ psd_mat.value)

    random_vector = np.random.randn(sdp_vectors.shape[1])
    random_vector /= np.linalg.norm(random_vector)
    colors = np.sign([vec @ random_vector for vec in sdp_vectors])
    score = colors @ laplacian @ colors.T

    return colors, score, bound

def maxcut_count(solution,adjancent_matrix):
    '''
    parameters
        solution: (1darray) 0/1 bitstring
        adjancent_matrix: (ndarray)
    return 
        count:(int) number of cutting edges
    '''
    m=adjancent_matrix
    n=adjancent_matrix.shape[0]
    count=0
    for i in range(n-1):
        for j in range(i+1,n):
            if solution[i]!=solution[j]:
                count+=m[i,j]
    return count

def brute_search(adjancent_matrix):
    '''
    parameter
        adjancent_matrix: adjancent matrix for maxcut
    return 
        (soultions,flag): configuration for the maxcut problem and the cutting edge count
    '''
    def bitstring(n):
        if n>1:
            return ['0'+bits for bits in bitstring(n-1)]+['1'+bits for bits in bitstring(n-1)]
        elif n==1:
            return ['0','1']
        else:
            print('error')

    m=adjancent_matrix
    n=m.shape[0]
    flag=0
    solutions=[]
    for conf in bitstring(n):
        sol=np.array(list(map(int,list(conf))))
        # print(sol)
        count=maxcut_count(sol,adjancent_matrix)
        if count==flag:
            solutions.append(conf)
        elif count>flag:
            solutions=[conf]
            flag=count
    return (solutions,flag)

# if __name__ == '__main__':
#     from classical_algorithm.random_graph_generator import gen_random_adjancent_matrix

#     n=4
#     G = nx.to_networkx_graph(gen_random_adjancent_matrix(n))
#     laplacian = np.array(0.25 * nx.laplacian_matrix(G).todense())
#     bound = goemans_williamson(G)[2]

#     print(goemans_williamson(G))

#     scores = [goemans_williamson(G)[1] for n in range(100)]

#     print(min(scores), max(scores))

#=========================================
# if __name__=="__main__":
#     import numpy as np
#     adj_m=np.array(list(map(float,"0.000000000000000000e+00 1.000000000000000000e+00 0.000000000000000000e+00 1.000000000000000000e+00 0.000000000000000000e+00 1.000000000000000000e+00 0.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 0.000000000000000000e+00 1.000000000000000000e+00 0.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 0.000000000000000000e+00 1.000000000000000000e+00 0.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 0.000000000000000000e+00".split(" "))))
#     adj_m=adj_m.reshape((5,5))
#     print(adj_m)
#     config=[0, 0, 0, 0, 0]
#     # print(maxcut_count(config,adj_m))
#     print(brute_search(adj_m))