
from TeXableEntity import TeXableEntity
class Privilege(TeXableEntity):
    """A function from G, v -> {True, False}

    >>> pred = Privilege(lambda G, v: v in G,
    ... # doctest: +SKIP
                         'G, v \mapsto v \in G',
                         'Returns true when $v$ is a node in $G$')
    >>> doc(pred)
    ... # doctest: +SKIP
    'Returns true when $v$ is a node in $G$'
    >>> repr(pred)
    ... # doctest: +SKIP
    'G, v \mapsto v \in G'
    """
    def __init__(self, predicate = lambda graph, node: True,
                       as_TeX    = None,
                       doc       = None):
        TeXableEntity.__init__(self, as_TeX, doc)
        self.predicate = predicate

    def __call__(self, graph, node):
        return self.predicate(graph, node)

    def __bool__(self, graph, node):
        return self()
