from ssa import Predicate, Move, Rule, Algorithm, CLIParser
import networkx as nx
import random

### Poor man's tests ###

# algorithms should be creatable from any callable object,
# so try just plain ole' functions
def mark(node):
    node['marked'] = True
    return node
def unmark(node):
    node['marked'] = False
    return node
def _mark_info(node, neighbors):
    marked = node['marked']
    neighbor_marked = any(map(lambda n: n['marked'], neighbors))
    return (marked, neighbor_marked)
def can_mark(node, neighbors):
    (marked, neighbor_marked) = _mark_info(node, neighbors)
    return not (marked or neighbor_marked)
def must_unmark(node, neighbors):
    (marked, neighbor_marked) = _mark_info(node, neighbors)
    return marked and neighbor_marked

def rand_graph(dimen):
    """Generate an arbitrary graph with 'marked' attributes."""
    graph = nx.grid_2d_graph(dimen, dimen)
    for node in graph.nodes:
        graph.node[node]['marked'] = random.choice([False, True])
    return graph

def run_test(algorithm):
    """Run an algorithm."""
    (stable, timeline) = algorithm.run(rand_graph(5), 1000)
    # after 1000 iterations, it's incredibley unlikely we've not
    # stablized a graph of only 25 nodes.  if this becomes a problem
    # with CI, the test can just be restarted.
    assert(stable)
    timeline.report()
    print(f"Stable? {stable}")

# test with predicates defined in code
print("from memory")
run_test(Algorithm([Rule(can_mark, mark), Rule(must_unmark, unmark)]))
