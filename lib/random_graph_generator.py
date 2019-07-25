import numpy as np
import matplotlib.pylab as plt
from numpy.random import rand

'''
use this script to generate N random graphs with n nodes

the graph is a list of random 2-tuples, in form of {(x1,y1), (x2,y2)...}

you can use the gen_graph() function to generate a single graphor run the code in the main() part to generate a long list of points

you can extract the graph as a list from the saved file using graph_decipher() function

saved in target file named as 'random_graph.csv' in current directory

'''

def gen_random_adjancent_matrix(n,symmetric=True,threshold=0.7):
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


def generate_adj_matrix(N,n,save_file):
    print("generating random adjancent matrix...")
    data = []
    for i in range(N):
        data.append(gen_random_adjancent_matrix(n).flatten())
    np.savetxt(save_file, np.array(data, dtype=int))

def gen_graph(n=6,scale=100):
    '''
    n: number of vertices in the graph
    scale: scale factor of the graph, 100 as default
    return: a n*2 2-d array, contains all the n vertices in the graph
    in a coordinate form (x,y)
    '''
    points=[(np.random.rand(),np.random.rand()) for i in range(n)]
    return scale*np.array(points)


def graph_plot(graph):
    '''
    visualize the graph given by the gen_graph function
    '''
    X=graph[:,0]
    Y=graph[:,1]
    plt.scatter(X,Y)
    plt.show()

def graphs_decipher(target_file,n=6):
    '''
    extract graphs from a long randomly generated list of 2-tuples 
    (saved in a file as 2-D numpy array) 

    target_file: file name of the saved array
    return a list of 2*n array
    '''
    data=np.loadtxt(target_file)
    N=data.shape[0]//n
    graphs=[]
    for i in range(N):
        graphs.append(data[i*n:(i+1)*n])
    return graphs

def get_distance_matrix(array):
    '''
    given a set of vertices of a graph in form of n*2 array (x,y)
    return a n*n distance matrix for this graph (suppose it's all connected)
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


if __name__=='__main__':
    n=6 # node number of graph
    N=20 # number of graph generated
    target_file="random_graphs.csv"
    
    test=True
    print("generating graphs...")
    
    graphs=[]
    for i in range(N):
        graph=gen_graph(n)
        graphs.append(graph)
    print("finished!")

    graphs=np.vstack(graphs)
    np.savetxt(target_file,graphs)
    print("graphs saved!")
    
    if test:
        graph_plot(graphs_decipher(target_file)[0])
        print("successfully extract graphs!")
    