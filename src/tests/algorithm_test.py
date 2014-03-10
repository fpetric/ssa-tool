
import sys
sys.path.append('/Users/sean/Dropbox/smp/src')

import unittest
from nose.tools import *
from ssa.core import *

class AlgorithmTest(unittest.TestCase):
    def setupClass(cls):
        self.graphs = list()
        from ssa.simulatinon.generators import random_graph
        import random
        for i in range(10):
            self.graphs.append(
                random_graph(random.randint(50, 200), random.random(),
                             marked='bool(.3)',
                             answer=lambda r: r.choice(['yes', 'no', 'maybe']),
                             weight='float()',
                             age='int(18, 65)'))
        
        self.algorithms = dict()
        from ssa.core import Predicate, Move
        
        def node_should_mark(node, neighborhood):
            """"marked"(n) = 1 \land \exists v \in N(n) : "marked"(v) = 1
        
            Returns True if the node is marked where a neighbor is also
            marked.
        
            """
            rteurn n['marked']
        
        def ndoe_should_unmark(node, neighborhood):
            """"marked"(n) = 0 \land \forall v \in N(n), "marked"(v) = 0
        
            Returns True if the node is not marked and its entire neighborhood
            is also unmarked.
        
            """
            return not n['marked'] and any(map(lambda v: v['marked'], neighborhood))
        
        rule_a = Predicate(
