import networkx as nx
import random
import copy

# A Executable (and particular types Predicate and Move) are runnable
# objects read from disk.
class Executable:
    """Generic container for callables read from disk."""
    CODE_INDENT = 4

    def __init__(self, name, source_file, parameters, code_transform=None):
        """Create a new Executable.

        - `source_file`: a canonicalized file containing code
        - `parameters`: a list of parameter names assumable by `source_file`

        """
        self.name = name
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
        if not self._func:
            self._define()
        return self._func(*params)

    def __repr__(self):
        """Give a reasonable representation of this `Executable`.

        - What kind of executable am I?
        - Where am I in memory?
        - self.name
        - self.source_file (source file)
        """
        return f"<{self.__class__.__name__} at {hex(id(self))} - \'{self.name}\' from \"{self.source_file}\">"

    def __str__(self):
        return f"<{self.__class__.__name__} '{self.name}'>"

    def _define(self):
        """Read `self.source_file` and load it into memory."""
        with open(self.source_file) as f:
            self._code_lines = f.readlines()

        lines = self._code_lines

        # run transform (e.g., add a return statement for Move objects)
        # default is to do nothing
        if self._code_transform:
            lines = self._code_transform(lines)

        # indent the definition to prepare to evaluate
        lines = [(" " * Executable.CODE_INDENT) + l for l in lines]

        # add the definition line
        params_signature = ",".join(self.parameters)
        lines = ["def indirect_executable(" + params_signature + "):\n"] + lines

        # evalute the code and maintain a reference to the function in memory
        exec("".join(lines), locals())
        self._func = locals()["indirect_executable"]

class Predicate(Executable):
    """A Boolean-valued function of a node and its neighbors.

    Code for these functions has access to two symbols:

    - `v`: attributes for a node
    - `N`: neighborhood of `v`

    """
    def __init__(self, name, definition):
        super().__init__(name, definition, ["v", "N"])

class Move(Executable):
    """A function called for effect on a node.

    Code for these functions has access to the symbol `v`, the
    attributes of the privileged node.

    """
    def __init__(self, name, definition):
        super().__init__(name, definition, ["v"], lambda lines: lines + ["return v"])

class Rule:
    """A predicate-move pair."""
    def __init__(self, predicate, move):
        """Create a new rule.

        - `predicate`: a boolean-valued callable of two arguments: a
        dictionary of node attributes and a list of dictionaries of
        neighbors' attributes.

        - `move`: a dictionary-valued callable of one argument: a
        dictionary of node attributes.  Should return the new state of
        a node passed in (i.e., a new dictionary).

        """
        self.predicate = predicate
        self.move = move

    def applies_to(self, node, neighbors):
        """True if this rule applies to a node given its neighbors.

        This looks to the rule's predicate to make the determination.

        """
        return self.predicate(node, neighbors.values())

    def apply_to(self, node):
        """Apply this rule to a node.

        Uses this rule's move for effect on `node`.

        """
        return self.move(node)

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
        def __init__(self, rule, node, new_data):
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

    def __init__(self, base):
        self._base = base
        self._end = None
        self._steps = list()
        self._stable = False

    def add_step(self, rule, node, new_data):
        self._steps.append(GraphTimeline.Step(rule, node, new_data))

    def report(self):
        print(f"Initial state: {self._base.nodes.data()}")
        for step in self._steps:
            print(f"{step.rule.move} {step.node}")
        print(f"Steps: {len(self._steps)}")

class Algorithm:
    def __init__(self, rules):
        for r in rules: assert(isinstance(r, Rule))
        self.rules = rules

    def run(self, graph, max_steps=None):
        """Run an algorithm on a graph.

        Returns a tuple of

        - 0: True if `graph` stabilized
        - 1: a `GraphTimeline` instance for the run

        """
        timeline = GraphTimeline(graph)
        working_graph = copy.deepcopy(graph)
        stable = False
        current_step = 0

        while not stable and (max_steps is None or current_step < max_steps):
            (privileged_node, rule) = self.pick_node_under_rule(working_graph)
            if privileged_node is None:
                # if no nodes are privileged, we've stabilized
                stable = True
            else:
                current_step += 1

                # get the new data for the node by applying the rule
                new_data = rule.apply_to(working_graph.node[privileged_node])

                # record what happened in the timeline
                timeline.add_step(rule, privileged_node, new_data)

        return (stable, timeline)

    def find_privileged_nodes(self, graph):
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
            neighbors = {v: graph.node[v] for v in graph.neighbors(node)}

            # search for applicable rules
            for rule in self.rules:
                if rule.applies_to(graph.node[node], neighbors):
                    applicable_rules.append(rule)

            # record any applicable rules in the dictionary
            if applicable_rules:
                privileged[node] = (neighbors, applicable_rules)
        return privileged

    def pick_node_under_rule(self, graph):
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

# helper function to generate a random graph with the appropriate
# attributes
def rand_graph():
    graph = nx.grid_2d_graph(3, 3)
    for node in graph.nodes:
        graph.node[node]['marked'] = random.choice([False, True])
    return graph

if __name__ == "__main__":
    def run_test(algorithm):
        (stable, timeline) = algorithm.run(rand_graph(), 1000)
        timeline.report()
        print(f"Stable? {stable}")

    # functions load from file correctly
    p_unmark = Predicate("unmark", "examples/ind-set.ssax/predicates/marked-and-neighbor-marked.py")
    assert(    p_unmark({'marked': True},  [{'marked': True}]))
    assert(not p_unmark({'marked': False}, [{'marked': False}]))

    # test __repr__ and __str__
    assert("at 0x" in repr(p_unmark))
    assert("at 0x" not in str(p_unmark))

    p_mark = Predicate("mark", "examples/ind-set.ssax/predicates/unmarked-and-neighbors-unmarked.py")
    m_unmark = Move("unmark", "examples/ind-set.ssax/moves/unmark.py")
    m_mark = Move("mark", "examples/ind-set.ssax/moves/mark.py")

    # test with predicates defined in code
    print("from memory")
    run_test(Algorithm([Rule(can_mark, mark), Rule(must_unmark, unmark)]))

    print()

    # test with predicates/moves loaded from disk into memory with `Executable`
    print("from disk")
    run_test(Algorithm([Rule(p_mark, m_mark), Rule(p_unmark, m_unmark)]))

# Local Variables:
# python-shell-interpreter: "python3"
# python-indent-offset: 4
# End:
