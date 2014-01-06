
from TeXableEntity import TeXableEntity
class Action(TeXableEntity):
    """A function from G, v -> G'

    >>> action = Action(lambda G, v: v['marked'] = True,
    ... # doctest: +SKIP
                        'v.marked \gets True',
                        'Marks $v$')
    >>> doc(action)
    ... # doctest: +SKIP
    'Mark $v$'
    >>> repr(action)
    ... # doctest: +SKIP
    'v.marked \gets True'
    """
    def __init__(self, action = lambda graph, node: graph,
                       as_TeX = None,
                       doc    = None):
        TeXableEntity.__init__(self, as_TeX, doc)
        self.action = action

    def __call__(self, graph, node):
        return self.action(graph, node)
