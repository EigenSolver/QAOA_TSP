from lib.random_graph_generator import graphs_decipher,get_distance_matrix
from lib.tsp_solver import held_karp

n=4
data_file="./data/random_graphs.txt"
solution_file="./data/tsp_solutions_n={}.txt".format(n)

graphs=graphs_decipher(data_file,n)
print("graphs loaded...")

solution_set=[]
N=len(graphs)

count=0
for g in graphs:
    solution_set.append(held_karp(get_distance_matrix(g)))
    count+=1
    if count%10==0:
        print("solving TSP...{0}/{1}".format(count,N))

print("writing solutions...")
with open(solution_file,'w') as f:
    for solution in solution_set:
        f.write(str(solution)+"\n")
print("finished!")