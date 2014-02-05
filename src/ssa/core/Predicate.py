
from TeXableEntity import TeXableEntity
class Predicate(TeXableEntity):
    """A function from G, v -> {True, False}

       A `Predicate` consists of two parts:
       
         - documentation (both TeXnical and human-readable)
       
               >>> TeX_documentation   = 'G, v \mapsto \dots'
               >>> human_documentation = 'Returns true when $v$ has' +
                                         'more than one marked neighbor.'
       
         - predicate function, which can be a pure 'lambda' function:
       
               >>> lambda_predicate = lambda G, v: v in G
       
           or the name of a full-on function:
       
               >>> def fulldef_predicate(graph, node):
               ...     number_marked = 0
               ...     for neighbor in graph.neighbors(node):
               ...         if neighbor.marked:
               ...             number_marked += 1
               ...         if number_marked > 1:
               ...             return True
               ...     return False
       
       We can create a `Predicate` object using these three parts like so:
       
           >>> predicate = Predicate(fulldef_predicate,
           ...                       TeX_documentation,
           ...                       human_documentation)
       
       Our `Predicate` object will now behave like a function, able to be
       called with two arguments (a graph and a node) for a natural feel.
       Let's create a random graph and get a random node in that graph;
       hopefully we'll get lucky!
       
           >>> from generators import random_graph
           >>> from random import choice
           >>> G = random_graph(              \
                 (20, 30),                    \
                 .8,                          \
                 marked='bool(.8)')
           >>> some_node = choice(G.nodes())
       
       Now that we have `G` and `some_node` in `G`, we can test to see if the
       predicate is true for that node in `G`:
       
           >>> predicate(G, some_node)                   # doctest: +SKIP
           True
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
