
import sys
sys.path.append('/Users/sean/Dropbox/smp/src')

import unittest
from nose.tools import *
from core.Algorithm import Algorithm
from core.Algorithm import predicate
from core.Algorithm import move
from simulation.generators import random_graph
import random

class AlgorithmTest(unittest.TestCase):
    @classmethod
    def setupClass(cls):
        cls.graphs = list()
        for i in range(10):
            cls.graphs.append(
                random_graph(random.randint(50, 200), random.random(),
                             marked='bool(.3)',
                             answer=lambda r: r.choice(['yes', 'no', 'maybe']),
                             weight='float()',
                             age='int(18, 65)'))
        
        cls.algorithm = dict()
        @predicate(author='Sean Allred', version='1.0')
        def node_should_unmark(node, neighborhood):
            """Rule 1
        
            "marked"(n) = 1 `land `exists v `in N(n) : "marked"(v) = 1
        
            Returns True if the node is marked where a neighbor is also
            marked.
        
            """
            return n['marked'] and any(map(lambda v: v['marked'], neighborhood))
        
        @predicate(author='Sean Allred', version='1.0')
        def node_should_mark(node, neighborhood):
            """Rule 2
        
            "marked"(n) = 0 `land `forall v `in N(n), "marked"(v) = 0
        
            Returns True if the node is not marked and its entire neighborhood
            is also unmarked.
        
            """
            return not n['marked'] and all(map(lambda v: not v['marked'], neighborhood))
        @move(author='Sean Allred', version='1.0')
        def mark_node(node, neighborhood):
            node['marked'] = True
            return node, neighborhood
        
        @move(author='Sean Allred', version='1.0')
        def unmark_node(node, neighborhood):
            node['marked'] = False
            return node, neighborhood
        
        cls.algorithm['independent set'] = \
        Algorithm({
             node_should_mark: [mark_node],
           node_should_unmark: [unmark_node]
        })

    def test_metadata(self):
        pred = self.algorithm['independent set'].ruleset.keys()[0]
        assert pred.meta['name']      != ''
        assert pred.meta['doc tex']   != ''
        assert pred.meta['doc human'] != ''
