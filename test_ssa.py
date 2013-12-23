"""
Base class for self-stabilizing algorithms.

"""

__author__ = "\n".join(["Sean Allred (seallred@smcm.edu)"])

from networkx import SelfStabilizingAlgorithm as SSA

#class SelfStabilizingAlgorithm:
#    def __init__(self, rules=dict()):
#        pass
#    def add_rule(self, predicate=lambda graph, privileged_node: True,
#                       action=lambda graph, privileged_node: graph):
#        pass
#    def apply_to(graph, count=1, keep_history=False):
#        pass

class SelfStabilizingAlgorithmTest:
    def __init__(self):
        self.randomly_marked = Graph()

    def ind_set(self):
        independent_set = SSA()

        def any_marked(graph, node):
            return any(lambda n: n.marked, graph.neighbors(node)) and not node.marked
        def none_marked(graph, node):
            return all(lambda n: not n.marked, graph.neighbors(node)) and node.marked
        def mark_node(graph, node):
            node.marked = True
            return graph
        def unmark_node(graph, node):
            node.marked = False
            return graph
        
        independent_set.add_rule(any_marked, unmark_node)
        independent_set.add_rule(none_marked, mark_node)
        
        
