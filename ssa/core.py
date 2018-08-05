import networkx as nx
import random
import copy
import logging
from typing import List, Callable, NewType, Optional, Dict, Tuple, Union, cast, Any

TNode = NewType("TNode", object)
TNodeData = NewType("TNodeData", object)
TPred = Callable[[TNodeData, List[TNodeData]], bool]
TMove = Callable[[TNodeData], TNodeData]

# A Executable (and particular types Predicate and Move) are runnable
# objects read from disk.
class Executable:
    """Generic container for callables read from disk."""
    CODE_INDENT = "    "

    name: str
    source_file: str
    parameters: List[str]

    _code_transform: Optional[Callable[[List[str]], List[str]]]
    _func: Optional[Callable]
    _code_lines: Optional[List[str]]

    def __init__(self, source_file: str, parameters: List[str], code_transform: Optional[Callable[[List[str]], List[str]]] = None) -> None:
        """Create a new Executable.

        - `source_file`: a canonicalized file containing code
        - `parameters`: a list of parameter names assumable by `source_file`

        """
        self.parameters = parameters
        self.source_file = source_file
        self._code_transform = code_transform
        self._func = None
        self._code_lines = None

    def __call__(self, *params):
        """Run the code from `self.source_file` with `params`.

        - `params`: a list of values corresponding to `self.parameters`.

        Executable code may modify `params`, so it may be wise to
        perform `copy.deepcopy` if that should not be allowed.

        """
        self.ensure_resolved()
        return self._func(*params)

    def __repr__(self):
        """Give a reasonable representation of this `Executable`.

        - What kind of executable am I?
        - Where am I in memory?
        - self.name
        - self.source_file (source file)
        """
        return f"<{self.__class__.__name__} at {hex(id(self))} - \"{self.source_file}\">"

    def __str__(self):
        return f"<{self.__class__.__name__} '{self.source_file}'>"

    def ensure_resolved(self):
        """If the source file has not been read form disk, do so."""
        if not self._func:
            self._define()

    def _define(self):
        """Read `self.source_file` and load it into memory."""
        logging.debug(f"Loading {self.source_file}")
        with open(self.source_file) as f:
            # we can't reliably depend on a terminating newline,
            # so strip them all and add them back later
            self._code_lines = [s.rstrip() for s in f.readlines()]

        lines: List[str]
        lines = self._code_lines

        # run transform (e.g., add a return statement for Move objects)
        # default is to do nothing
        if self._code_transform:
            lines = self._code_transform(lines)

        # indent the definition to prepare to evaluate
        lines = [Executable.CODE_INDENT + l for l in lines]

        # add the definition line
        params_signature: str
        params_signature = ",".join(self.parameters)
        lines = ["def indirect_executable(" + params_signature + "):"] + lines

        # evalute the code and maintain a reference to the function in memory
        exec("\n".join(lines), locals())
        self._func = locals()["indirect_executable"]

class Predicate(Executable):
    """A Boolean-valued function of a node and its neighbors.

    Code for these functions has access to two symbols:

    - `v`: attributes for a node
    - `N`: neighborhood of `v`

    """
    def __init__(self, definition: str) -> None:
        super().__init__(definition, ["v", "N"])

class Move(Executable):
    """A function called for effect on a node.

    Code for these functions has access to the symbol `v`, the
    attributes of the privileged node.

    """
    def __init__(self, definition: str) -> None:
        super().__init__(definition, ["v"], lambda lines: lines + ["return v"])

class Rule:
    """A predicate-move pair."""

    predicate: TPred
    move: TMove

    def __init__(self, predicate: TPred, move: TMove) -> None:
        """Create a new rule.

        - `predicate`: a boolean-valued callable of two arguments: a
        dictionary of node attributes and a list of dictionaries of
        neighbors' attributes.

        - `move`: a dictionary-valued callable of one argument: a
        dictionary of node attributes.  Should return the new state of
        a node passed in (i.e., a new dictionary).

        """
        # ignore typing on the stuff below (see python/mypy#708)
        self.predicate = predicate # type: ignore
        self.move = move           # type: ignore

    def applies_to(self, node: TNodeData, neighbors: List[TNodeData]):
        """True if this rule applies to a node given its neighbors.

        This looks to the rule's predicate to make the determination.

        """
        return self.predicate(node, neighbors) # type: ignore

    def apply_to(self, node):
        """Apply this rule to a node.

        Uses this rule's move for effect on `node`.

        """
        return self.move(node)  # type: ignore

    def __repr__(self):
        return f"<Rule at {hex(id(self))} - {repr(self.predicate)} to {repr(self.move)}>"

    def __str__(self):
        return f"<Rule {self.predicate} to {self.move}>"

class GraphTimeline:
    """A graph over time.

    Keeps a step-by-step history of an algorithm's run on a graph.

    """
    # todo: implement __iter__ to yeild graphs at steps
    class Step:
        def __init__(self, rule: Rule, node: TNode, new_data: TNodeData) -> None:
            """Create a new 'step'.

            - `rule`: the `Rule` object that applied to `node`
            - `node`: the node that moved
            - `new_data`: the new data `node` was given

            """
            self.rule = rule
            self.node = node
            self.new_data = new_data

        def __repr__(self):
            return f"<Step at {hex(id(self))} - {repr(self.rule)} on {repr(self.node)} yeilds {repr(self.new_data)}>"

        def __str__(self):
            return f"<Step {self.rule} on {self.node} yeilds {self.new_data}>"

    def __init__(self, base: nx.Graph) -> None:
        self._base = base
        self._end: Optional[nx.Graph] = None
        self._steps: List[GraphTimeline.Step] = list()
        self._stable = False

    def add_step(self, rule: Rule, node: TNode, new_data: TNodeData) -> None:
        self._steps.append(GraphTimeline.Step(rule, node, new_data))

    def report(self):
        print(f"Initial state: {dict(self._base.nodes.data())}")
        for step in self._steps:
            print(f"{step.rule.move} {step.node}")
        print(f"Steps: {len(self._steps)}")

class Algorithm:
    def __init__(self, rules: List[Rule]) -> None:
        self.rules = rules

    def run(self, graph: nx.Graph, max_steps: int = None) -> Tuple[bool, GraphTimeline]:
        """Run an algorithm on a graph.

        Returns a tuple of

        - 0: True if `graph` stabilized
        - 1: a `GraphTimeline` instance for the run

        """
        timeline = GraphTimeline(graph)
        working_graph = copy.deepcopy(graph)
        stable = False
        current_step = 0

        privileged_node: Optional[TNode]
        rule: Optional[Rule]

        while not stable and (max_steps is None or current_step < max_steps):
            (privileged_node, rule) = self.pick_node_under_rule(working_graph)
            if privileged_node is None:
                # if no nodes are privileged, we've stabilized
                stable = True
            else:
                current_step += 1

                # we know there are values here now
                # related: python/mypy#4805
                privileged_node = cast(TNode, privileged_node)
                rule = cast(Rule, rule)

                # get the new data for the node by applying the rule
                new_data = rule.apply_to(working_graph.node[privileged_node])

                # record what happened in the timeline
                timeline.add_step(rule, privileged_node, new_data)

        return (stable, timeline)

    def find_privileged_nodes(self, graph: nx.Graph) -> Dict[TNode, Tuple[List[TNodeData], List[Rule]]]:
        """Find and return the 'privileged' nodes in `graph`.

        Privileged nodes are those nodes in the graph that satisfy one
        or more predicates.  The return value is a dictionary of these
        privileged nodes and a tuple:

        - 0: the neighbors of the node used for calculation
        - 1: a list of the rules (predicate-move pairs) that were satisfied.

        """
        privileged = dict()
        # This loop could potentially be slow: nodes * neighbors * rules
        # (not even counting the predicate logic)
        for node in graph:
            applicable_rules = []

            # collect neighbor data for the predicate
            neighbors = cast(List[TNodeData], # satisfy type-checker
                             {v: graph.node[v] for v in graph.neighbors(node)}.values())

            # search for applicable rules
            for rule in self.rules:
                if rule.applies_to(graph.node[node], neighbors):
                    applicable_rules.append(rule)

            # record any applicable rules in the dictionary
            if applicable_rules:
                privileged[cast(TNode, node)] = (neighbors, applicable_rules)
        return privileged

    def pick_node_under_rule(self, graph: nx.Graph) -> Tuple[Optional[TNode], Optional[Rule]]:
        """Find one node in `graph` to which a rule applies.

        Return a tuple (node, rule).

        """
        privileged_nodes = self.find_privileged_nodes(graph)
        if not privileged_nodes:
            return (None, None)

        # pick a privileged node at random to move
        lucky_node = random.choice(list(privileged_nodes.keys()))

        # of the applicable rules, choose one at random
        (_neighbors, applicable_rules) = privileged_nodes[lucky_node]
        lucky_rule = random.choice(applicable_rules)

        return (lucky_node, lucky_rule)

    def ensure_resolved(self):
        """Load all rules defined from disk into memory.

        When doing parallel processing with the same Algorithm instance,
        this will avoid race conditions where a I/O may be performed twice.

        """
        for rule in self.rules:
            for exe in [rule.predicate, rule.move]:
                if isinstance(exe, Executable):
                    exe.ensure_resolved()
