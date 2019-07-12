import numpy as np
import matplotlib.pylab as plt

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

'''
use this script to generate N random graphs with n nodes
target file is named as 'random_graph.csv', saved in current directory
'''

if __name__=='__main__':
    n=6 # node number of graph
    N=2 # number of graph generated
    gen_graphs=[]
    for i in range(N):
        graph=gen_graph(n)
        graph_plot(graph)
        gen_graphs.append(graph)

    gen_graphs=np.array(gen_graphs)
    
    # print(gen_graphs)

    np.savetxt('random_graphs.csv',gen_graphs)