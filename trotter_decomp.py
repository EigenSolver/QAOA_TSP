from projectq.backends import Simulator, CommandPrinter, ResourceCounter

from projectq.cengines import (AutoReplacer,
                               LocalOptimizer,
                               TagRemover,
                               DecompositionRuleSet)

from projectq import MainEngine
from projectq.types import Qubit, Qureg
from projectq.ops import QubitOperator, Allocate, TimeEvolution, All, Measure, Swap
from projectq.setups import decompositions
from projectq.setups.decompositions import time_evolution


backend = Simulator()
printer = CommandPrinter()
conuter = ResourceCounter()

cache_depth = 10
rule_set = DecompositionRuleSet(modules=[decompositions])
# rule_set.add_decomposition_rule(time_evolution)

engines = [TagRemover(), LocalOptimizer(cache_depth),
           AutoReplacer(rule_set), TagRemover(),
           LocalOptimizer(cache_depth), CommandPrinter()]

eng = MainEngine(Simulator(), engines)
state = eng.allocate_qureg(2)
op = QubitOperator("Z0")
Swap | (state[0],state[1])
eng.flush()
All(Measure) | state
del state
print(rule_set.decompositions.keys())
