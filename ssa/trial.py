import networkx as nx
import random
from typing import Callable, Dict, List, Tuple, Any, Optional
import concurrent.futures
import logging
from collections import OrderedDict

import ssa

def apply_properties(graph: nx.Graph, property_generators: Dict[str, Callable[[], Any]]) -> nx.Graph:
    """Apply properties to a graph given a dictionary of properties."""
    for node in graph.nodes:
        n = graph.node[node]
        for prop in property_generators:
            n[prop] = property_generators[prop]()
    return graph

def get_value_generator(member: str):
    """Find a property-value generator by a given name."""
    return globals()['genp_'+member] # GENerate Property

def get_graph_generator_parser(member: str):
    """Find a graph generator by a given name."""
    return globals()['geng_'+member] # GENerate Graph

# define functions that consume the argument piece in the spec
# and return a function that returns a random graph.
# (we need this layer of indirection to avoid creating the graph
# too early).  only required and optional-named parameters are
# supported (i.e., no keyword arguments).
def geng_gn(number_of_nodes: str):
    """Return a graph-generator that gives a graph of a set number of nodes."""
    return lambda: nx.generators.gn_graph(int(number_of_nodes))

def geng_gnm(number_of_nodes: str, number_of_edges: str):
    """Return a graph-generator that gives a graph of a set number of nodes and edges."""
    return lambda: nx.generators.gnm_random_graph(int(number_of_nodes), int(number_of_edges))

def genp_bool() -> Callable[[], bool]:
    """Random boolean generator."""
    return lambda: random.random() <= 0.5

def genp_choice(*choices: list):
    """Random element from choices."""
    return lambda: random.choice(choices)

def genp_rangef(min: str, max: str) -> Callable[[], float]:
    """Random real in range [min, max)."""
    if min == '0' and max == '1':
        return random.random
    minf = float(min)
    return lambda: random.random() * (float(max) - minf) + minf

def genp_range(min: str, max: str) -> Callable[[], int]:
    """Random integer in range [min, max]."""
    return lambda: random.randint(int(min), int(max))

def run(algorithm: ssa.Algorithm, graph_generator: Callable[[], nx.Graph], num_iterations: int, num_graphs: int, timeout_seconds: int = 120, workers: int = 32) -> Dict[bool, List[ssa.GraphTimeline]]:
    """Run an algorithm many, many times in parallel.

    - algorithm: the algorithm to run
    - graph_generator: a function of no arguments that returns a graph
    - num_iterations: maximum number of iterations of the algorithm per graph
    - num_graphs: number of graphs to generate

    - timeout_seconds: after this many seconds, an algorithm will abort
    - workers: number of workers (threads) to use

    The return value is keyed by whether or not the algorithm
    stabilized.  The value is a list of run histories.

    """
    results: Dict[bool, List[ssa.GraphTimeline]] = {True: [], False: []}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        algorithm.ensure_resolved()
        futures = [executor.submit(lambda: algorithm.run(graph_generator(), num_iterations)) \
                   for i in range(num_graphs)]
        for f in futures:
            try:
                result = f.result(timeout_seconds)
                results[result[0]].append(result[1])
            except TimeoutError:
                logging.warning("One of the results timed out!")
    return results
