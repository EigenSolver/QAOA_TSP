import projectq.setups.decompositions as rules

from projectq.backends import Simulator

from projectq.cengines import (AutoReplacer,
                               LocalOptimizer,
                               TagRemover,
                               DecompositionRuleSet)

from projectq import MainEngine



backend = Simulator(gate_fusion=True)

cache_depth = 10
rule_set = DecompositionRuleSet(modules=[rules])
engines = [TagRemover()
            , LocalOptimizer(cache_depth)
            , AutoReplacer(rule_set)
            , TagRemover()
            , LocalOptimizer(cache_depth)
            ]

eng = MainEngine(backend, engines)