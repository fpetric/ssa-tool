
from ssa.core import TeXableEntity
from ssa.core import Predicate
from ssa.core import Action
class Algorithm(TeXableEntity):
    """A self-stabilizing algorithm

    
    """
    def __init__(self, TeX,
                       doc,
                       pa):
        self.TeX = TeX
        self.doc = doc
        self.pa  = pa

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
