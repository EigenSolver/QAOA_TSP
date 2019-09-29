from projectq import MainEngine
from projectq.backends import CircuitDrawer
from projectq.ops import *
import os
from optimizeq import QuantumCircuit

drawer=CircuitDrawer()
eng=MainEngine(drawer)

with open("./circuits/TSP_circuit_n=4_p=1.txt") as f:
    circ=QuantumCircuit(f.readlines())

qureg = eng.allocate_qureg(circ.qubit_num)

for cmd in circ.cmd_list:
    if "Allocate" in cmd or "Deallocate" in cmd:
        continue
    else:
        eval(cmd.replace("Qureg", "qureg"))
eng.flush()

with open("./tsp_plot.tex","w") as f:
    f.write(drawer.get_latex())