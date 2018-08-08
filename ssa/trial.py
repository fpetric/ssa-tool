import networkx as nx
import random
from typing import Callable, Dict, List, Tuple, Any, Optional
import concurrent.futures
import logging
from collections import OrderedDict

import ssa

def description(description):
    """Decorator.  Describe this generator."""
    def decorator(func):
        func.description = description
        return func
    return decorator

def arg(name, description):
    """Decorator.  Describe the arguments to this generator."""
    def decorator(func):
        if not hasattr(func, 'arg_description'):
            func.arg_description = dict()
        func.arg_description[name] = description
        return func
    return decorator

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

def get_generators(prefix: str):
    """Get a list of all known generators."""
    # we actually return an OrderedDict from this function, but there's a bug in Python
    # that tries to evaluate the type as a real Type, which is not subscriptable.
    import sys, inspect
    symbol: str
    ret = dict()

    # get all the functions in the current module
    members = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
    for (symbol, code_object) in members:
        if symbol.startswith(prefix+"_"):
            # if the symbol name begins with our prefix, get the
            # overall and argument descriptions and put a tuple in our
            # dictionary.
            (_, name) = symbol.split("_", 1)
            args = OrderedDict(_get_signature_arguments(code_object))
            fn_doc = _get_function_description(code_object)
            ret[name] = (fn_doc, args if len(args) > 0 else None)
    return ret

def _get_function_description(function_code_object) -> str:
    """Get a description for the function."""
    if hasattr(function_code_object, 'description'):
        return function_code_object.description
    import inspect
    return inspect.getdoc(function_code_object)

def _get_signature_arguments(function_code_object) -> List[Tuple[str, Optional[str]]]:
    """Get descriptions for all arguments of the function."""
    import inspect
    signature = inspect.signature(function_code_object)
    ret = list()
    if not hasattr(function_code_object, 'arg_description'):
        # type-ignore because mypy thinks signature.parameters is a
        # list of strings, but in fact it's a list of Parameter
        # objects
        return [(p.name, None) for p in signature.parameters] # type: ignore

    param: inspect.Parameter
    for param in signature.parameters.values():
        name = param.name
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            name += "..."
        ret.append((name, function_code_object.arg_description[param.name] if param.name in function_code_object.arg_description else None))
    return ret

# define functions that consume the argument piece in the spec
# and return a function that returns a random graph.
# (we need this layer of indirection to avoid creating the graph
# too early).  only required and optional-named parameters are
# supported (i.e., no keyword arguments).
@description("Generate a random graph with a set number of nodes")
@arg("number_of_nodes", "The graph generated will have this many nodes")
def geng_gn(number_of_nodes: str):
    """Return a graph-generator that gives a graph of a set number of nodes."""
    return lambda: nx.generators.gn_graph(int(number_of_nodes))

@description("Generate a random graph with a set number of nodes and edges")
@arg("number_of_nodes", "The graph generated will have this many nodes")
@arg("number_of_edges", "The graph generated will have this many edges")
def geng_gnm(number_of_nodes: str, number_of_edges: str):
    """Return a graph-generator that gives a graph of a set number of nodes and edges."""
    return lambda: nx.generators.gnm_random_graph(int(number_of_nodes), int(number_of_edges))

@description("A random boolean")
def genp_bool() -> Callable[[], bool]:
    """Random boolean generator."""
    return lambda: random.random() <= 0.5

@description("A random choice")
@arg("choices", "a list of choices")
def genp_choice(*choices: list):
    """Random element from choices."""
    return lambda: random.choice(choices)

@description("A random real number")
@arg("min", "the minimum possible value, inclusive")
@arg("max", "the maximum possible value, exclusive")
def genp_rangef(min: str, max: str) -> Callable[[], float]:
    """Random real in range [min, max)."""
    if min == '0' and max == '1':
        return random.random
    minf = float(min)
    return lambda: random.random() * (float(max) - minf) + minf

@description("A random integer")
@arg("min", "the minimum possible value, inclusive")
@arg("max", "the maximum possible value, exclusive")
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
