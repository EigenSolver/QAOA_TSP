# -*- coding: utf-8 -*-
import os 


os.chdir("..")
n=6 # node number of graph
N=20 # number of graph generated
target_file="./data/random_graphs.txt"

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
    