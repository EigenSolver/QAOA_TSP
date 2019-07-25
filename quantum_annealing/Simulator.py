#Yongcheng Ding
#Path Integral Quantum Monte Carlo Simulation for Quantum Annealing
#Most functions are written for solving TSP which requires modifications for solving other problems
import numpy as np
import itertools
import math
import random
from six import iteritems, itervalues
from random_graph_generator import graphs_decipher
from tsp_dp_solver import get_distance_matrix

#read the dataset 
n=6
target_file="random_graphs.csv"
graphs=graphs_decipher(target_file,n)
distance_matrix=get_distance_matrix(graphs[0])
trotter_number=10
T=0.1


#given a distance matrix, generate a QUBO matrix
def Distance_to_QUBO(distance_matrix):
    '''
    This could be used for generate the QUBO input for D-Wave
    Input: distance_matrix as 2d np array
    Output: QUBO as a dictionary
    '''
    node={}
    coupler_constraint_sum_i={}
    coupler_constraint_sum_s={}
    coupler_distance={}
    coupler_boundary={}
#qubits are encoded by q_{(i,a)}, i in 1,...,6 and a in 1,...,6
#penalty strength 100\sqrt{2}
    lamb=145
    mu=145
    for i in range (1,n+1):
        for s in range (1,n+1):
            node[(i,s),(i,s)]=-lamb-mu
#constraint condition \sum_i q_i,s=1
    for s in range (1,n+1):
        for i in range (1,n+1):
            for j in range (i+1,n+1):
                coupler_constraint_sum_i[(i,s),(j,s)]=2*lamb
#constraint condition \sum_s q_i,s=1
    for i in range (1,n+1):
        for s in range (1,n+1):
            for t in range(s+1,n+1):
                coupler_constraint_sum_s[(i,s),(i,t)]=2*mu
#for cost function
    for i in range (1,n+1):
        for j in range (1,n+1):
            for s in range (1,n):
                if i!=j:
                    coupler_distance[(i,s),(j,s+1)]=distance_matrix[i-1][j-1]
#for boundary into consideration
    for i in range (1,n+1):
        for j in range (1,n+1):
            if i!=j:
                coupler_boundary[(i,1),(j,n)]=distance_matrix[i-1][j-1]
#generate QUBO
    QUBO={}
    QUBO.update(node)
    QUBO.update(coupler_constraint_sum_i)
    QUBO.update(coupler_constraint_sum_s)
    QUBO.update(coupler_distance)
    QUBO.update(coupler_boundary)
    return QUBO

#given a QUBO, generate a spin-1/2 Hamiltonian
def QUBO_to_Ising(QUBO,offset=0.0):
    '''
    Thanks D-Wave :)
    Input: QUBO as a dict for the problem Hamiltonian
    Output: h, J, and offset as the spin-1/2 problem Hamiltonian, tuple
    '''
    h = {}
    J = {}
    linear_offset = 0.0
    quadratic_offset = 0.0
    for (u, v), bias in iteritems(QUBO):
        if u == v:
            if u in h:
                h[u] += 0.5 * bias
            else:
                h[u] = 0.5 * bias
            linear_offset += bias
        else:
            if bias != 0.0:
                J[(u, v)] = 0.25 * bias
            if u in h:
                h[u] += 0.25 * bias
            else:
                h[u] = 0.25 * bias
            if v in h:
                h[v] += 0.25 * bias
            else:
                h[v] = 0.25 * bias
            quadratic_offset += bias
    offset += 0.5 * linear_offset + 0.25 * quadratic_offset
    return h, J, offset

#initial state of 3D classical spin preparation
def Initial_state(n,trotter_number):
    '''
    Generate a 3d ap array of Z for random distribution
    Each trotter slice has the same configuration
    Input: site n, trotter_number
    Output Z site i site j trotter k
    '''
    Z=np.zeros((n,n,trotter_number))
    for i in range (0,n):
        for j in range (0,n):
#            for k in range (0,trotter_number):
            Z[i,j,:]=random.randint(0,1)*2-1
    return Z

#flip a spin at position Z[i][j][j]
def Spin_flip(Z,i,j,k):
    '''
    Flip a spin at (i,j,k)
    Input:Z,i,j,k
    Output:Z_candidate as 3d np array
    '''
    Z_candidate=Z.copy()
    Z_candidate[i][j][k]=-Z_candidate[i][j][k]
    return Z_candidate

#generate the trotterlized 3D classial spin Hamiltonian
def Ising_to_3D(H_2D,A,B,trotter_number):
    '''
    Generate a 3D classical spin Hamiltonian by Suzuki-Trotter theorem
    Input:
        H_2D: tuple [0] h dict [1] J dict [2] offset
        A: weight for tunneling Hamiltonian (traverse field)
        B: weight for problem Hamiltonian
        trotter_number
    Output:
        H_3d h dict J dict J_bot dict
    '''
    # h_3D
    h={}
    for i in range (1,n+1):
        for j in range (1,n+1):
            for k in range (1,trotter_number+1):
                h[(i,j,k)]=B*H_2D[0][(i,j)]
    # J_3D
    J={}
    ising_constraint_sum_i={}
    ising_constraint_sum_s={}
    ising_distance={}
    ising_boundary={}
    for k in range (1,trotter_number+1):
        for s in range (1,n+1):
            for i in range (1,n+1):
                for j in range (i+1,n+1):
                    ising_constraint_sum_i[(i,s,k),(j,s,k)]=B*H_2D[1][(i,s),(j,s)]
        for i in range (1,n+1):
            for s in range (1,n+1):
                for t in range(s+1,n+1):
                    ising_constraint_sum_s[(i,s,k),(i,t,k)]=B*H_2D[1][(i,s),(i,t)]
        for i in range (1,n+1):
            for j in range (1,n+1):
                for s in range (1,n):
                    if i!=j:
                        ising_distance[(i,s,k),(j,s+1,k)]=B*H_2D[1][(i,s),(j,s+1)]
        for i in range (1,n+1):
            for j in range (1,n+1):
                if i!=j:
                    ising_boundary[(i,1,k),(j,n,k)]=B*H_2D[1][(i,1),(j,n)]
    J.update(ising_constraint_sum_i)
    J.update(ising_constraint_sum_s)
    J.update(ising_distance)
    J.update(ising_boundary)
    # J_bot_3D
    jbot= -(trotter_number*T/2)*math.log(math.tanh(A/(trotter_number*T)))
    J_bot={}
    ising_trotter_coupler={}
    ising_trotter_boundary={}
    for i in range (1,n+1):
        for j in range (1,n+1):
            for k in range (1,trotter_number):
                ising_trotter_coupler[(i,j,k),(i,j,k+1)]=jbot
    for i in range (1,n+1):
        for j in range (1,n+1):
            ising_trotter_boundary[(i,j,1),(i,j,trotter_number)]=jbot
    J_bot.update(ising_trotter_coupler)
    J_bot.update(ising_trotter_boundary)
    return h, J, J_bot

#value the energy of a 3D Hamiltonian with a classical spin config
def Value_H_3D(H_3D,Z):
    '''
    Calculate the energy of a 3D classical spin Hamiltonian
    Could be very inefficient if the size grows larger
    Input:
        H_3D (1,...,n,1,...,n,1,...,trotter_number),Z(0,...,n-1,0,...,n-1,0,...,trotter_number-1)
    Output:
        Energy_3D
    '''
    #calculate the contribution of h_3D
    energy_h=0
    for k in range (0,trotter_number):
        for i in range(0,n):
            for j in range (0,n):
                energy_h+=H_3D[0][(i+1,j+1,k+1)]*Z[i][j][k]
    #calculate the contribution of J_3d
    energy_J=0
    for k in range (0,trotter_number):
        for s in range (0,n):
            for i in range (0,n):
                for j in range (i+1,n):
                    energy_J+=H_3D[1][(i+1,s+1,k+1),(j+1,s+1,k+1)]*Z[i][s][k]*Z[j][s][k]
        for i in range (0,n):
            for s in range (0,n):
                for t in range (s+1,n):
                    energy_J+=H_3D[1][(i+1,s+1,k+1),(i+1,t+1,k+1)]*Z[i][s][k]*Z[i][t][k]
        for i in range (0,n):
            for j in range (0,n):
                for s in range (0,n-1):
                    if i!=j:
                        energy_J+=H_3D[1][(i+1,s+1,k+1),(j+1,s+2,k+1)]*Z[i][s][k]*Z[j][s+1][k]
        for i in range (0,n):
            for j in range (0,n):
                if i!=j:
                    energy_J+=H_3D[1][(i+1,1,k+1),(j+1,n,k+1)]*Z[i][0][k]*Z[j][n-1][k]
    #calculate the contribution of J_bot
    energy_J_bot=0
    for i in range (0,n):
        for j in range (0,n):
            for k in range (0,trotter_number-1):
                energy_J_bot-=H_3D[2][(i+1,j+1,k+1),(i+1,j+1,k+2)]*Z[i][j][k]*Z[i][j][k+1]
    for i in range (0,n):
        for j in range (0,n):
            energy_J_bot-=H_3D[2][(i+1,j+1,1),(i+1,j+1,trotter_number)]*Z[i][j][0]*Z[i][j][trotter_number-1]
    energy=0
    energy=energy_h+energy_J+energy_J_bot
    return energy

#metropolis
def Metropolis(Z,i,j,k,H_3D,T):
    '''
    Obtain the accpeted 3D spin config after flipping a spin with metropolis
    Input:
        Z as the spin config to be flipped
        i, j, k for the spin to be flipped
        H_3D
        T temperature for metropolis
    Output:
        Z_accepted, energy accepted
    '''
    Z_candidate=Spin_flip(Z,i,j,k)
    energy_before_flip=Value_H_3D(H_3D,Z)
    energy_after_flip=Value_H_3D(H_3D,Z_candidate)
    delta=energy_before_flip-energy_after_flip
    if delta >= 0:
        Z_accepted=Z_candidate.copy()
        energy_accepted=energy_after_flip
    else:
        dice=random.random()
        if math.exp(delta/T) >= dice:
            Z_accepted=Z_candidate.copy()
            energy_accepted=energy_after_flip
        else:
            Z_accepted=Z.copy()
            energy_accepted=energy_before_flip
    return Z_accepted, energy_accepted

#find the best one among all layers.
def Find_best_layer(Z,QUBO):
    '''
    Obtain the best solution
    Transform the spin config of each layer to 0-1 qubit
    Find the minimum value (total cost) among all layers
    Input:
        Z final 3d config of spins
        QUBO matrix for the TSP
    Output:
        best_traveling_trajectory as 2d np array
        best_cost_efficient: there is a deviation between the efficient best cost and the minimum of objective function 
    ''' 
    qubit=np.zeros((n,n,trotter_number))          
    for i in range (0,n):
        for j in range (0,n):
            for k in range (0,trotter_number):
                if Z[i][j][k] == 1:
                    qubit[i][j][k]=1
                else:
                    qubit[i][j][k]=0
    cost_for_all_layers=np.zeros(trotter_number)
    for k in range (0,trotter_number):
        for i in range (0,n):
            for s in range (0,n):
                cost_for_all_layers[k]+=QUBO[(i+1,s+1),(i+1,s+1)]*qubit[i][s][k]
        for s in range (0,n):
            for i in range (0,n):
                for j in range (i+1,n):
                    cost_for_all_layers[k]+=QUBO[(i+1,s+1),(j+1,s+1)]*qubit[i][s][k]*qubit[j][s][k]
        for i in range (0,n):
            for s in range (0,n):
                for t in range (s+1,n):
                    cost_for_all_layers[k]+=QUBO[(i+1,s+1),(i+1,t+1)]*qubit[i][s][k]*qubit[i][t][k]
        for i in range (0,n):
            for j in range (0,n):
                for s in range (0,n-1):
                    if i!=j:
                        cost_for_all_layers[k]+=QUBO[(i+1,s+1),(j+1,s+2)]*qubit[i][s][k]*qubit[j][s+1][k]
        for i in range (0,n):
            for j in range (0,n):
                if i!=j:
                    cost_for_all_layers[k]+=QUBO[(i+1,1),(j+1,n)]*qubit[i][0][k]*qubit[j][n-1][k]
    min_index=np.argmin(cost_for_all_layers)
    best_traveling_trajectory=qubit[:,:,min_index]
    best_cost_effective=min(cost_for_all_layers)
    return best_traveling_trajectory, best_cost_effective

#let's start quantum annealing!

#problem formulation
Q=Distance_to_QUBO(distance_matrix)
H_2D=QUBO_to_Ising(Q,offset=0.0)
#Annealing schedule
A=np.array([100,50,25,10,5,2.5,1,0.5,0.25,0.1,1e-9])
B=np.array([1e-9,0.001,0.0025,0.005,0.01,0.025,0.05,0.1,0.25,0.5,1])
Z=Initial_state(n,trotter_number)
for qa_step in range (0,len(A)):
    H_3D=Ising_to_3D(H_2D,A[qa_step],B[qa_step],trotter_number)
    for i in range(0,n):
        for j in range (0,n):
            for k in range (0,trotter_number):
                Z=Metropolis(Z,i,j,k,H_3D,T)[0].copy()
    print('quantum annealing simulator goes for next field config',qa_step+1,'/',len(A))
#decoding
best_trajectory=Find_best_layer(Z,Q)[0]
print(best_trajectory)
best_cost=0
for i in range (0,n):
    for j in range (0,n):
        for s in range (0,n):
            if i!=j:
                if s<n-1:
                    distance=distance_matrix[i][j]*best_trajectory[i][s]*best_trajectory[j][s+1]
                else:
                    distance=distance_matrix[i][j]*best_trajectory[i][0]*best_trajectory[j][n-1]
                best_cost+=distance
print(best_cost)
