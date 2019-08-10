# Research on Quantum Approximate Optimization Algorithm versus Quantum Annealing on Travelling Salesman Problem


Collaborator: Yongcheng Ding, Yuning Zhang, Bin Cheng


## TSP Problems
- Quantum Annealing (D-Wave 2000Q)
- Quantum Approximate Optimization Algorithm(Huawei HiQ Simulator/IBM Europe or Rigetti 128 bit)
- Classical Algorithm (Dynamic Programming, Ant Colony Algorithm)

## Contents
- ./lib/: module library for the project 
- ./data/: data file generated by the execution script
- ./quantum_annealing/ : quantum annealing algorithm for TSP run on DWave quantum annealer
- ./references/ : shared ducuments, including research papers on recent progress of QAOA, technical documents of DWave annealer

### Library
- ./hiq_header: header that import all the dependency of hiq and initialize an hiq engine with SimulatorMPI 
- ./projectq_header: header that import all the dependency of project and initialize an projectq engine with SimulatorMPI 
- ./graph_converter: convert matrix to target Hamiltonian, including MAXCUT and TSP Hamiltonian
- ./random_graph_generator: generate random matrix data for QAOA and classical algorithm
- ./tsp_solver: Held-Karp algorithm
- ./maxcut_solver: Goemans-Williamson algorithm and a brute search
- ./qaoa_simple: a naive implementation of Quantum Approximate Optimization Algorithm
- ./utilities: helper module that provide some functional features in numerical test such as timer and progress printing

