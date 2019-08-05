from lib.random_graph_generator import gen_random_adjancent_matrix
import numpy as np
import networkx as nx
from lib.maxcut.goemans_williamson import goemans_williamson



    N = 200
    n = 5
    save_file = "./data/random_adjancent_matrix.txt"
    solution_file = "./data/maxcut_solution.txt"
    # generate_adj_matrix(N,n,save_file)

    data = np.loadtxt(save_file)
    N = data.shape[0]
    n = int(np.sqrt(data.shape[1]))

    print("generating solutions...")
    with open(solution_file, 'w') as f:
        for i in range(N):
            result = goemans_williamson(
                nx.to_networkx_graph(data[i, :].reshape((n, n))))
            if (i+1) % (N//10) == 0:
                print("progress: {0}/{1}".format(i+1, N))
            f.write(str(result)+"\n")
