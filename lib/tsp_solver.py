import itertools
import numpy as np


def tsp_cost(conf,dist_matrix):
    '''
    Args:
        conf(list): list of cities, ordered natrually
        dist_matrix(2darray): distance matrix
    Returns:
        cost(float): cost function
        
    >>> dist_m=np.array([[ 0.        , 90.51313794, 62.86696471, 50.75077802, 82.14307135],\
       [90.51313794,  0.        , 44.41743947, 91.82705138,  8.81303117],\
       [62.86696471, 44.41743947,  0.        , 48.06290502, 40.26546524],\
       [50.75077802, 91.82705138, 48.06290502,  0.        , 86.38368889],\
       [82.14307135,  8.81303117, 40.26546524, 86.38368889,  0.        ]])
    >>> conf=[4,2,1,3,0]
    >>> tsp_cost(conf,dist_m)
    309.40380546
    '''
    cost=0
    for i in range(len(conf)-1):
        cost+=dist_matrix[conf[i],conf[i+1]]
    cost+=dist_matrix[conf[0],conf[-1]]
    return cost

def tsp_bits_convert(bitstring):
    '''
    Args:
        bitstring(array): iterable of 0/1 bits
    Returns:
        configuration(list): list of ints, solution of tsp
    
    >>> tsp_bits_convert([0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1])
    [1, 0, 2, 3]
    '''
    n=np.sqrt(len(bitstring))
    assert n%1==0
    n=int(n)
    
    conf=[]
    mark=np.arange(n)
    for i in range(n):
        conf.append(np.sum(mark*bitstring[i*n:(i+1)*n]))
    return conf

def held_karp(dists):
    """
    from https://github.com/CarlEkerot/held-karp/blob/master/held-karp.py
    
    Implementation of Held-Karp, an algorithm that solves the Traveling
    Salesman Problem using dynamic programming with memoization.
    Parameters:
        dists: distance matrix
    Returns:
        A tuple, (cost, path).
    
    """
    n = len(dists)

    # Maps each subset of the nodes to the cost to reach that subset, as well
    # as what node it passed before reaching this subset.
    # Node subsets are represented as set bits.
    C = {}

    # Set transition cost from initial state
    for k in range(1, n):
        C[(1 << k, k)] = (dists[0][k], 0)

    # Iterate subsets of increasing length and store intermediate results
    # in classic dynamic programming manner
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            # Set bits for all nodes in this subset
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            # Find the lowest cost to get to this subset
            for k in subset:
                prev = bits & ~(1 << k)

                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prev, m)][0] + dists[m][k], m))
                C[(bits, k)] = min(res)

    # We're interested in all bits but the least significant (the start state)
    bits = (2**n - 1) - 1

    # Calculate optimal cost
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dists[k][0], k))
    opt, parent = min(res)

    # Backtrack to find full path
    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    # Add implicit start state
    path.append(0)

    return opt, list(reversed(path))


if __name__=='__main__':
#    from matplotlib.pylab import imshow
#    from lib.random_graph_generator import get_distance_matrix,gen_graph, graph_plot,graphs_decipher
#    
#    g=gen_graph(10)
#    # graph_plot(g)
#    m=get_distance_matrix(g)
#    # print(m)
#    
#    # graphs_decipher()
#    sol=held_karp(m)
#    print(sol)
    import doctest
    doctest.testmod()
