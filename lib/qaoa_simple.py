import projectq as pq
from projectq import MainEngine
from projectq.ops import QubitOperator, Measure, All, H, X, TimeEvolution
from projectq.meta import Loop

import numpy as np
import scipy as sp


class QAOA(object):
    def __init__(self, engine, H_cost, n_qubits, n_steps=3,
                 H_mixer=None, ansatz_func=None,
                 init_betas=[], init_gammas=[]):

        if not init_betas:
            self.init_betas = np.linspace(0, np.pi, n_steps)
        if not init_gammas:
            self.init_gammas = np.linspace(0, 2*np.pi, n_steps)
        self.engine = engine # global
        self.n_qubits = n_qubits 
        self.n_steps = n_steps
        self.H_cost = H_cost
        self.H_mixer = H_mixer or self.default_mixer() # directly revoke 
        
        # pass constructive function
        self.ansatz_func = ansatz_func or self.default_ansatz 
 
        self.result=None
        self.solution=None
        self.min_cost=None
    
    # just a sub function! not a method
    def default_ansatz(self, engine,n_qubits):
        ansatz = engine.allocate_qureg(n_qubits)
        All(X) | ansatz # important- ground state!
        All(H) | ansatz
        return ansatz
    
    def default_mixer(self):
        # generate mixer Hamiltonian
        H_mixer = 0*QubitOperator("")
        for i in range(self.n_qubits):
            H_mixer += QubitOperator("X{}".format(i))
        return H_mixer

    def cost_expectation(self, params):
        # extract beta & gamma
        betas = params[:self.n_steps]
        gammas = params[self.n_steps:]
        # generate initial state
        state = self.ansatz_func(self.engine,self.n_qubits)
        
        # evolution
        for i in range(self.n_steps): # optimization
            TimeEvolution(gammas[i], self.H_cost) | state
            TimeEvolution(betas[i], self.H_mixer) | state
        #
        self.engine.flush()

        # each time before the qubit is measured the 
        expectation = self.engine.backend.get_expectation_value(self.H_cost, state)
        All(Measure) | state
        return expectation


    def optimize(self,method="TNC"):#"COBYLA"
        params0 = np.hstack((self.init_betas, self.init_gammas))
        bounds=[(0, np.pi) for i in range(self.n_steps)]+[(0, 2*np.pi) for j in range(self.n_steps)]

        self.result=sp.optimize.minimize(self.cost_expectation, \
            params0, method=method,bounds=bounds)

    def get_result(self):
        return self.result
    
    def get_solution(self, draw=10):
        params=self.result.x
        betas = params[:self.n_steps]
        gammas = params[self.n_steps:]

        self.min_cost=None
        self.solution=[]
        for i in range(draw):
            state = self.ansatz_func(self.engine,self.n_qubits)
            
            # evolution
            for i in range(self.n_steps): # optimization
                TimeEvolution(gammas[i], self.H_cost) | state
                TimeEvolution(betas[i], self.H_mixer) | state
            
            All(Measure)|state
            self.engine.flush()
            cost=self.engine.backend.get_expectation_value(self.H_cost,state)
            if self.min_cost is None:
                self.min_cost=cost
            elif self.min_cost>cost:
                self.min_cost=cost
                self.solution=[int(qb) for qb in state]
        
        return (self.solution,self.min_cost)


# test pass  
# if __name__ == "__main__":
#     from graph_converter import MAXCUT_Hamiltonian
#     from ProjectQ_header import *


#     save_file="random_adjancent_matrix.csv"
#     data=np.loadtxt(save_file)
#     N=data.shape[0]
#     n=int(np.sqrt(data.shape[1]))
    
#     H_cost=MAXCUT_Hamiltonian(data[0,:].reshape((n,n)))

#     qaoa=QAOA(eng,H_cost,n,n_steps=1)
#     print('compile done...')
#     qaoa.optimize()
#     print(qaoa.get_result())
#     print(qaoa.get_solution())
    
