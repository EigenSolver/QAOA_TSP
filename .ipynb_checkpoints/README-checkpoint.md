# Research on Quantum Approximate Optimization Algorithm versus Quantum Annealing on Travelling Salesman Problem


Collaborator: Yongcheng Ding, Yuning Zhang, Bin Cheng


## TSP Problems
- Quantum Annealing (D-Wave 2000Q)
- Quantum Approximate Optimization Algorithm(Huawei HiQ Simulator/IBM Europe or Rigetti 128 bit)
- Classical Algorithm (Dynamic Programming, Ant Colony Algorithm)

## Contents
- ./classical_TSP/ : classical dynamical programming algorithm (Held-Karp) for TSP, give optimal solution as a benchmark
- ./quantum_annealing/ : quantum annealing algorithm for TSP run on DWave quantum annealer
- ./references/ : shared ducuments, including research papers on recent progress of QAOA, technical documents of DWave annealer