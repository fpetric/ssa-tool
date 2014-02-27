
import inspect

class Algorithm:
    """A self-stabilizing algorithm

    
    """
    #% algorithm %#
    def __init__(self, ruleset):
        self.ruleset = ruleset
    #% endalgorithm %#

        #% algorithm-ruleset-assertions %#
        assert hasattr(self.ruleset, '__getitem__')
        assert all(map(lambda p: hasattr(p, '__call__'),
                       self.ruleset))
        assert all(map(lambda p: Algorithm.is_valid_function(p),
                       self.ruleset))
        for predicate in self.ruleset:
            moves = self.ruleset[predicate]
            assert hasattr(moves, '__getitem__')
            assert all(map(lambda m: hasattr(m, '__call__') and
                                     Algorithm.is_valid_function(m),
                           moves))
        #% end-algorithm-ruleset-assertions %#

    def run(self, graph, count=1):
        """Run the algorithm `count` times.
    
        
        """
        assert count >= 0
    
        history = None
        while count > 0:
            privileged_nodes = dict()
            for node in graph.nodes:
                neighborhood = graph.neighbors(node)
                for predicate in self.ruleset:
                    if predicate(node, neighborhood):
                        if node in privileged_nodes:
                            privileged_nodes[node] += predicate
                        else:
                            privileged_nodes[node] = [predicate]
            node = random.choice(privileged_nodes)
            neighborhood = graph.neighbors(node)
            satisfied_predicate = random.choice(privileged_nodes[node])
            next_move = random.choice(self.ruleset[satisfied_predicate])
            new_node, new_neighborhood = next_move(node, neighborhood)
            history.add((node, neighborhood, next_move, new_node, new_neighborhood))

    def has_stabilized(self):
        """Returns True if the graph has stabilized.
    
        This function runs `Algorithm.run` twice."""
        pass

    
  
    def is_valid_function(function):
        return len(inspect.getargspec(function).args) is 2
