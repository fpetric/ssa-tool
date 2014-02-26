
import inspect
class Move:
    """A function from G, v -> G'

    Create an action like so:
    
        >>> action = Move(lambda G, v: v['marked'] = True,
                            'v.marked \gets True',
                            'Marks $v$')
    
    You can retrieve the documentation and TeX representation of the
    object as you would a `TeXableEntity`:
    
        >>> action.doc
        'Mark $v$'
        >>> action.TeX
        'v.marked \gets True'
    
    You can also *call* `Move` objects, passing a graph and node as
    arguments.  This functionality is deferred to the member function
    `Move.action`.
    """
    #% move %#
    def __init__(self, move):
        self.move = move

    def __call__(self, graph, node):
        return self.move(graph, node)
    #% endmove %#
