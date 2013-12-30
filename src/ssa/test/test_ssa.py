__author__ = "Sean Allred (seallred@smcm.edu)"

import networkx as nx
from ssa import SelfStabilizingAlgorithm

class SelfStabilizingAlgorithmTest:
    def __init__(self):
        self.randomly_marked = Graph()

    def ind_set(self, num_applications=15):
        independent_set = SelfStabilizingAlgorithm()

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

        random_graph = nx.Graph()

        for i in range(num_applications):
            independent_set.apply_to(random_graph)
            print(random_graph, data=True)

if __name__ == "__main__":
    test = SelfStabilizingAlgorithmTest()
    print('Testing independent set algorithm...')
    test.ind_set()
    print('Done test.')
