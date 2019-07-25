from classical_algorithm.random_graph_generator import gen_random_adjancent_matrix
import numpy as np
import networkx as nx
from goemans_williamson import goemans_williamson

N=200
n=5

save_file="random_adjancent_matrix.csv"

print("generating random adjancent matrix...")
data=[]
for i in range(N):
    data.append(gen_random_adjancent_matrix(n).flatten())
np.savetxt(save_file, np.array(data))

solution_file="maxcut_solution.csv"
data=np.loadtxt(save_file)
N=data.shape[0]
n=int(np.sqrt(data.shape[1]))

print("generating solutions...")
with open(solution_file,'w') as f:
    for i in range(N):
        result=goemans_williamson(nx.to_networkx_graph(data[0,:].reshape((n,n))))
        if (i+1)%(N//10)==0:
            print("progress: {0}/{1}".format(i+1,N))
        f.write(str(result)+"\n")