
from TeXableEntity import TeXableEntity
class Action(TeXableEntity):
    """A function from G, v -> G'

    Create an action like so:
    
        >>> action = Action(lambda G, v: v['marked'] = True,
                            'v.marked \gets True',
                            'Marks $v$')
    
    You can retrieve the documentation and TeX representation of the
    object as you would a `TeXableEntity`:
    
        >>> action.doc
        'Mark $v$'
        >>> action.TeX
        'v.marked \gets True'
    
    You can also *call* `Action` objects, passing a graph and node as
    arguments.  This functionality is deferred to the member function
    `Action.action`.
    """
    def __init__(self, action = lambda graph, node: graph,
                       as_TeX = None,
                       doc    = None):
        TeXableEntity.__init__(self, as_TeX, doc)
        self.action = action

    def __call__(self, graph, node):
        return self.action(graph, node)
