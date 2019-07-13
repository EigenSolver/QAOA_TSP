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

def graphs_decipher(target_file,n=6):
    '''

    '''
    data=np.loadtxt(target_file)
    N=data.shape[0]//n
    graphs=[]
    for i in range(N):
        graphs.append(data[i*n:(i+1)*n])
    return graphs

'''
use this script to generate N random graphs with n nodes

the graphs are vertically stacked into one big 2-D array

you can extract the graph as a list from the saved file using graph_decipher

saved in target file named as 'random_graph.csv' in current directory


'''

if __name__=='__main__':
    n=6 # node number of graph
    N=20 # number of graph generated
    test=True
    gen_graphs=[]
    print("generating graphs...")
    
    for i in range(N):
        graph=gen_graph(n)
        gen_graphs.append(graph)
    print("finished!")

    gen_graphs=np.vstack(gen_graphs)
    np.savetxt('random_graphs.csv',gen_graphs)
    print("graphs saved!")
    
    if test:
        target_file="random_graphs.csv"
        graph_plot(graphs_decipher(target_file)[0])
        print("successfully extract graphs!")
    