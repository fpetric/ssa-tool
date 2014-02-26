
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

        assert(hasattr(self.ruleset, '__getitem__'))
        assert(all(map(lambda p: hasattr(p, '__call__'),
                       self.ruleset)))
        assert(all(map(lambda p: len(inspect.getargspec(p).args) is 2,
                       self.ruleset)))
        for predicate in self.ruleset:
            moves = self.ruleset[predicate]
            assert(hasattr(moves, '__getitem__'))
            assert(all(map(lambda move: hasattr(move, '__call__') and
                                        len(inspect.getargspec(move).args) is 2,
                           moves)))            
  
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
