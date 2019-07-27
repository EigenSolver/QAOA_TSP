import projectq.setups.decompositions as rules
from projectq.cengines import (AutoReplacer,
                               LocalOptimizer,
                               TagRemover,
                               DecompositionRuleSet)

from hiq.projectq.cengines import GreedyScheduler, HiQMainEngine
from hiq.projectq.backends import SimulatorMPI

from mpi4py import MPI


backend = SimulatorMPI(gate_fusion=True, num_local_qubits=20)

cache_depth = 10
rule_set = DecompositionRuleSet(modules=[rules])
engines = [TagRemover()
            , LocalOptimizer(cache_depth)
            , AutoReplacer(rule_set)
            , TagRemover()
            , LocalOptimizer(cache_depth)
            , GreedyScheduler()
            ]

eng = HiQMainEngine(backend, engines)
