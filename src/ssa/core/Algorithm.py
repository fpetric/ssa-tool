
import inspect
import TeXableEntity
import Predicate
import Move

class Algorithm:
    """A self-stabilizing algorithm

    
    """
    #% algorithm %#
    def __init__(self, TeX, doc, ruleset):
        self.TeX = TeX
        self.doc = doc
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
        """Run the algorithm `n` times.
    
        
        """
        assert n >= 0
        while n > 0:
            pass

    def has_stabilized(self):
        """Returns True if the graph has stabilized.
    
        This function runs `Algorithm.run` twice."""
        pass

    
  
    def is_valid_function(function):
        return len(inspect.getargspec(function).args) is 2
