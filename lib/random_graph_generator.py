import numpy as np
from numpy.random import rand

'''
graph generator, this module is used to generate random matrix data for QAOA and classical algorithm

'''

def gen_random_adjancent_matrix(n,symmetric=True,threshold=0.7):
    '''
    generate a random adjancet matrix    
    
    Args:
        n(int): dimension of the square matrix
        symmetric(boolean): if the matrix is symmetric
        threshold(int): connection probability
    Returns:
        adj_matrix(ndarray): an adjancent matrix
    '''
    adj_matrix=np.zeros((n,n))
    for i in range(n-1):
        for j in range(i+1,n):
            if rand()<threshold:
                adj_matrix[i,j]=1
            if symmetric:
                adj_matrix[j,i]=adj_matrix[i,j]
            else:
                if rand()<threshold:
                    adj_matrix[j,i]=1
    return adj_matrix


def gen_random_points(n,scale=100):
    '''
    Args:
        n(int): number of vertices in the graph
        scale(int): scale factor of the graph, 100 as default
    Returns:
        (ndarray):a n*2 2-d array, contains all the n vertices in the graph
    in a coordinate form (x,y)
    '''
    points=[(np.random.rand(),np.random.rand()) for i in range(n)]
    return scale*np.array(points)


def get_distance_matrix(array):
    '''
    given a set of vertices of a graph in form of n*2 array (x,y)
    
    Args:
        array(ndarray): a n*2 2-d array, contains all the n vertices in the graph
    in a coordinate form (x,y)
    
    Returns:
        distance_matrix(ndarray): a n*n distance matrix for this graph (suppose it's all connected)
    '''
    def distance(p1,p2):
        return np.sqrt(np.sum((p1-p2)**2))

    n=array.shape[0]
    distance_matrix=np.zeros((n,n))

    for i in range(n):
        for j in range(i+1):
            distance_matrix[i,j]=distance(array[i,:],array[j,:])
            distance_matrix[j,i]=distance_matrix[i,j]

    return distance_matrix

#========================
    
def gen_adj_matr_list(save_file,N,n):
    '''
    generate random adjancent matrix list and save to file
    
    Args:
        save_file(str): path to save file
        N(int): length of list
        n(int): dimension of matrix
    Returns:
        None
    '''
    print("generating random adjancent matrix...")
    data = []
    for i in range(N):
        data.append(gen_random_adjancent_matrix(n).flatten())
    np.savetxt(save_file, np.array(data, dtype=int))
    

def gen_dist_matr_list(save_file,N,n,scale):
    '''
    generate random distance matrix list and save to file
    
    Args:
        save_file(str): path to save file
        N(int): length of list
        n(int): dimension of matrix
        scale(float): scaling ratio of distance
    Returns:
        None
    '''
    print("generating random distance matrix...")
    data = []
    for i in range(N):
        data.append(get_distance_matrix(gen_random_points(n,scale)).flatten())
    np.savetxt(save_file, np.array(data, dtype=int))
    
def decode_matrix_list(target_file,n):
    '''
    extract graphs from a long randomly generated list of 2-tuples 
    (saved in a file as 2-D numpy array) 
    Args:
        target_file(str): file name of the saved array
    Returns:
        graph(list): a list of 2*n array
    '''
    data=np.loadtxt(target_file)
    N=data.shape[0]
    graphs=[data[i,:].reshape((n,n)) for i in range(N)]
    return graphs

if __name__=="__main__":# test
    
    test_a=gen_random_points(6,100)
    print(test_a)
    print("a pass")
    
    test_b=gen_random_adjancent_matrix(5)
    print(test_b)
    print("b pass")
    
    test_c=get_distance_matrix(test_a)
    print(test_c)
    print("c pass")
    
    
    n=6
    N=3
    
    test_file1="test1.txt"
    gen_adj_matr_list(test_file1,N,n)
    
    
    test_file2="test2.txt"
    gen_dist_matr_list(test_file2,N,n,100)
    print("d pass")
    
    print(decode_matrix_list("test1.txt",n))
    print("e pass")
    print(decode_matrix_list("test2.txt",n))
    
    