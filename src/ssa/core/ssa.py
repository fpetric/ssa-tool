"""
Base class for self-stabilizing algorithms.

"""

__author__ = "\n".join(["Sean Allred (seallred@smcm.edu)"])

import networkx as nx
import random

class SelfStabilizingAlgorithm:
    """Base class for self-stabilizing algorithms.

    The SelfStabilizingAlgorithm class represents its namesake as a set
    of predicate-action pairs.  Both predicates and actions must be
    pure functions that take exactly two arguments:
    

    Parameters
    ----------
    graph : the graph
        The graph that you're working with.  Useful for getting
        information about neighbors, etc.
    privileged_node : acting node
        The node that triggered this action.

    Returns
    -------
    The new graph.

    (TODO: the `inspect` module can provide some safety) # against what??
"""
    def __init__(self, rules=dict()):
        self.rules = dict()

        for predicate in rules.keys():
            self.add_rule(predicate, rules[predicate])

    def add_rule(self, predicate=lambda graph, privileged_node: True,
                       action=lambda graph, privileged_node: graph):
        """Add a rule to this algorithm.

        Parameters
        ----------
        predicate : f: (graph, node) \to {True, False}
        action :    f: (graph, node) \to graph
        """
        if predicate in self.rules:
            self.rules[predicate].append(action)
        else:
            self.rules[predicate] = [action]

    def apply_to(graph, count=1, keep_history=False):
        """Apply this algorithm to `graph` `count` times.

        Algorithm
        ---------
        Initialize this history and the current graph.  For as many
        times specified by `count`, do the following:

           1. Create a set of nodes that we need to check in this round,
              initialized to the complete set of nodes currently in the
              graph. 
           2. While we have nodes to check,
              2.1 Randomly choose a privileged node from the set of
                  unchecked nodes.
              2.2 Create a set of all predicates that apply to the              # TODO: unnecessary to check them all
                  privileged node.
         *    2.3 If this set is not empty, choose a random predicate
                  from that set.  Otherwise, break out of the while
                  loop, leaving the matching predicate as a None-value
                  (see step 3).
              2.4 Remove this node from the set of unchecked nodes
         * 3. If the matching predicate is None, break.  There is no
              point in continuing to check since the state of the
              graph will no longer change.
           4. Retrieve the approriate action for the matching
              predicate.
           5. Update the current graph by applying the action
              appropriately.
           6. If we are keeping history, record the necessary elements
              and update the current graph to a deep copy of itself.

        (*) Represents a step where program flow may be redirected.

        Returns
        -------
        If `keep_history` is specified, the function will return a
        history (as a list of 3-tuples) that map the current state of
        the graph to the predicate and node that caused it.
        """
        history = [(graph, None, None)]

        if keep_history:
            current_graph = graph.copy()
        else:
            current_graph = graph

        for i in range(count):
            unchecked_nodes = current_graph.get_nodes()[:]

            privileged_node = None
            matching_predicate = None

            while unchecked_nodes:
                privileged_node = random.choice(unchecked_nodes)

                # I'm not using shuffle because "Note that for even
                # rather small len(x), the total number of
                # permutations of x is larger than the period of most
                # random number generators; this implies that most
                # permutations of a long sequence can never be
                # generated."
                preds = [p for p in self.rules.keys()]
                while preds:
                    matching_predicate = random.choice(preds)

                    if p(current_graph, privileged_node):
                        break

                    preds.remove(matching_predicate)

                unchecked_nodes.remove(privileged_node)

            if matching_predicate is None: break
            else:
                matching_action = random.choice(self.rules[matching_predicate])
                current_graph = matching_action(current_graph,
                                                privileged_node)

                if keep_history:
                    history.append((current_graph,
                                    matching_predicate,
                                    privileged_node))
                    current_graph = current_graph.copy()

        if keep_history:
            return history
        else:
            return graph
