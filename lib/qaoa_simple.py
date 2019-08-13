from projectq.ops import QubitOperator, Measure, All, H, X, TimeEvolution
import numpy as np
from scipy.optimize import minimize

class QAOA(object):
    def __init__(self, engine, H_cost, n_qubits, n_steps=3,
                 H_mixer=None, ansatz_func=None,
                 init_betas=[], init_gammas=[],n_sampling=0, cost_eval=None,verbose=False):
        '''
        initialize a QAOA instance
        
        Args:
            engine(MainEngine): engine of projectq or hiq
            H_cost(QubitOperator): cost Hamiltionian of problem
            n_qubits(int): number of qubits
            n_steps(int): p value in QAOA circuit depth
            H_mixer(QubitOperator:list): list of mixer Hamiltionian, given by operator ansatz technique, apply a time evolution by order
            ansatz_func(function(eng,n)): function of engine and qubits, initialze the ansatz of problem, given by operator ansatz technique
            init_betas(list): default parameters beta
            init_gammas(list): default parameters gamma
            n_sampling(int): sampling number to evaluate the cost of problem
            cost_eval(function): convert bitstring given by problem, return cost
        '''

        if not init_betas:
            self.__init_betas = np.linspace(0, np.pi, n_steps)
        if not init_gammas:
            self.__init_gammas = np.linspace(0, 2*np.pi, n_steps)
        self.__engine = engine # global
        self.__n_qubits = n_qubits 
        self.__n_steps = n_steps
        self.__H_cost = H_cost
        self.__verbose=verbose
        self.__iter_count=0
        
        self.__H_mixer = H_mixer or self.__default_mixer() # directly revoke 
        # pass constructive function
        self.__ansatz_func = ansatz_func or self.__default_ansatz 
        
        # ensure cost_eval is given if sampling result
        
        self.__n_sampling = n_sampling
        self.__cost_eval = cost_eval
            
 
        self.__result=None
        self.__solution=None
        self.__min_cost=None
    
    # just a sub function! not a method
    def __default_ansatz(self, engine,n_qubits):
        ansatz = engine.allocate_qureg(n_qubits)
        All(X) | ansatz # important- ground state!
        All(H) | ansatz
        return ansatz
    
    def __default_mixer(self):
        # generate mixer Hamiltonian
        H_mixer = 0*QubitOperator("")
        for i in range(self.__n_qubits):
            H_mixer += QubitOperator("X{}".format(i))
        return [H_mixer]
    
    def __prep_state(self, params):
        # extract beta & gamma
        betas = params[:self.__n_steps]
        gammas = params[self.__n_steps:]
        # generate initial state
        state = self.__ansatz_func(self.__engine,self.__n_qubits)
        
        # evolution
        for i in range(self.__n_steps): # optimization
            TimeEvolution(gammas[i], self.__H_cost) | state
            for H_mixer in self.__H_mixer:
                TimeEvolution(betas[i], H_mixer) | state
        return state
    
    def __cost_expectation(self, params):
        '''
        tricky part 
        '''

        # on real quantum device, we can only obtain the expectation of an Hamiltonian via sampling measurements!
        if self.__n_sampling:
            expectation = 0
            for i in range(self.__n_sampling):
                state=self.__prep_state(params)
                All(Measure)|state
                self.__engine.flush()
                expectation+=self.__cost_eval([int(qb) for qb in state])/self.__n_sampling
                del state
                
        else:
            state=self.__prep_state(params)
            self.__engine.flush()
            expectation = self.__engine.backend.get_expectation_value(self.__H_cost, state)
            All(Measure) | state
            del state # to be determined
        
        if self.__verbose:
            self.__iter_count+=1
            print("iteration:",self.__iter_count)
            
        return expectation


    def run(self,method="COBYLA",options=None):
        params0 = np.hstack((self.__init_betas, self.__init_gammas))
        bounds=[(0, np.pi) for i in range(self.__n_steps)]+[(0, 2*np.pi) for j in range(self.__n_steps)]

        self.__result=minimize(self.__cost_expectation, \
            params0, method=method,bounds=bounds,options=options)
        return self.__result
    
    @property
    def iter_count(self):
        return self.__iter_count
    
    @property
    def result(self):
        if self.__result is None:
            raise ValueError("please run QAOA first")
        else:
            return self.__result
    
    
    def get_solution(self,draw=10):
        '''
        Args:
            draw(int): number of sampling
        Returns:
            configuration(list): bitstring represent the final state after optimization
            cost(float): value of cost function
        '''
        if self.__result is not None:
            params=self.__result.x
        else:
            print("please run QAOA first")

        self.__min_cost=None
        self.__solution=[]
        
        if self.__n_sampling:
            draw=self.__n_sampling # replace default parameter
        
        for i in range(draw):
            state=self.__prep_state(params)
            All(Measure)|state
            self.__engine.flush()
            conf=[int(qb) for qb in state]
            if self.__n_sampling:
                cost=self.__cost_eval(conf)
            else:
                cost=self.__engine.backend.get_expectation_value(self.__H_cost,state)
            
            if self.__min_cost is None:
                self.__min_cost=cost
            elif self.__min_cost>cost:
                self.__min_cost=cost
                self.__solution=conf
            del state
            
        return (self.__solution,self.__min_cost)

