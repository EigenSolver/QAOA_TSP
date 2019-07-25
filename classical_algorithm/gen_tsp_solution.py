from random_graph_generator import graphs_decipher
from tsp_dp_solver import get_distance_matrix,held_karp

n=6
target_file="random_graphs.csv"
graphs=graphs_decipher(target_file,n)
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
solution_file="tsp_solutions.txt"
with open(solution_file,'w') as f:
    for solution in solution_set:
        f.write(str(solution)+"\n")
print("finished!")