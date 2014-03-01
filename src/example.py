from ssa.core import *
from ssa.simulation.generators import random_graph

import networkx

G = random_graph(5, marked='bool(.25)')

def read_neighbors(G, n):
    return {n: G.node[n] for n in G.neighbors(n)}

n = G.nodes()[1]
print(repr(read_neighbors(G, n)))

def is_marked_alone(node, neighborhood=None):
    if node['marked']:
        for n in neighborhood:
            if n['marked']:
                return n
        else:
            return True
    return False
