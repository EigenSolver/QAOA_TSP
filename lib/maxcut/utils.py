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
#=========================================
if __name__=="__main__":
    import numpy as np
    adj_m=np.array(list(map(float,"0.000000000000000000e+00 1.000000000000000000e+00 0.000000000000000000e+00 1.000000000000000000e+00 0.000000000000000000e+00 1.000000000000000000e+00 0.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 0.000000000000000000e+00 1.000000000000000000e+00 0.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 0.000000000000000000e+00 1.000000000000000000e+00 0.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 0.000000000000000000e+00".split(" "))))
    adj_m=adj_m.reshape((5,5))
    print(adj_m)
    config=[0, 1, 0, 1, 0]
    print(maxcut_count(config,adj_m))