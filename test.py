import ssa
import networkx as nx

print('Starting')
print('Creating bundle')
b = ssa.Bundle('examples/ind-set.ssax')
print('accessing algorithm')
a = b.sorted()[-1]

print('creating star graph')
n=5
G = nx.star_graph(n-1)
print('marking graph as appropriate')
for d in G.node:
    G.node[d]['marked'] = False
G.node[1]['marked'] = True
from pprint import pprint
print('current graph:')
pprint(G.nodes(data=True))
print('running algorithm n times')
h=a.run(G, n)
print('history:')
pprint(h)
print('graph:')
pprint(G.nodes(data=True))
print('done')
