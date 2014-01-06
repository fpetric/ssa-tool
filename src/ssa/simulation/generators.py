
import networkx
import random
from itertools import combinations

class BasicNode:
    def __init__(self):
        pass
    def __repr__(self):
        return '{}::{}'.format(id(self), self.__dict__)

def random_graph(degree, edge_probability=0.5, base_class=BasicNode, **properties):
    """Generates a random graph of `degree` nodes, a specified
    probability for edges, and a number of random properties.
    
    If `degree` is a tuple, it is assumed to be a (min, max) tuple
    defining an inclusive range of possible degrees.
      
    Each `properties` value can be a function of a random number
    generator.  If the value does not have `__call__` defined, it will be
    assumed a string unless, as a string, it is one of the following:
      
    - 'int(n,m)' :: a random integer in [n, m]
    - 'float()'  :: a random floating point number in [0, 1)
    - 'bool(n)'  :: a random boolean with a probability of truth between 0
                    and 1 inclusive (where 1 is True).
      
    If the property value is neither callable nor a string of this form,
    then the value is simply set raw.

    Pass in a single argument, the degree of the graph, to get the
    bare-minimum graph (with a certain edge probability):
      
        >>> G = random_graph(50)
        >>> len(G.nodes())
        50
    
    Pass in a tuple to get a range of values:
      
        >>> G = random_graph((40, 60))
        >>> len(G.nodes()) in range(40, 60 + 1)
        True
      
    You can also use a few intelligent arguments, such as bool(n):
    
        >>> G = random_graph(10, marked='bool(1)')
        >>> all(map(lambda n: G.node[n]['marked'], G.node))
        True
        >>> G = random_graph(10, marked='bool(0)')
        >>> any(map(lambda n: G.node[n]['marked'], G.node))
        False
      
    float():
    
        >>> G = random_graph(1000, weight='float()')
        >>> .45 < sum(map(lambda n: G.node[n]['weight'], G.node)) / 1000 < .55
        True
      
    and int(min, max):
      
        >>> G = random_graph(10, age='int(40, 50)')
        >>> all(map(lambda n: G.node[n]['age'] in range(40, 50 + 1), G.node))
        True
    
    For any attribute, you can specify a function or a generator.  You can
    even supply a function that *returns* a generator.  All functions must
    take exactly one required argument, a random number generator, as its
    first parameter.
    
    (ref:smp - optionify random thingy)
    
    Consider the following:
    
        >>> graph = random_graph(5, weight=(i for i in range(5)))
        >>> sorted([graph.node[n]['weight'] for n in graph.nodes()])
        [0, 1, 2, 3, 4]
    
                                                                             (ref:)

    Be careful about the arguments you pass.  If you want a range of
    possible values for the degree, ensure you pass an iterable of exactly
    two elements.
      
        >>> random_graph((1,2,3))
        Traceback (most recent call last):
          File "<stdin>", line 1, in ?
        ValueError: Wrong number of values for (min, max) degree
      
    Mind the arguments for the keywords 'bool', 'int', and 'float'.
      
        >>> random_graph(5, marked='int(3,4,5)')
        Traceback (most recent call last):
          File "<stdin>", line 1, in ?
        ValueError: Wrong number of arguments for int.
    
    If you are using generators, keep in mind that *each* node must be
    given a value.  If the generator produces less values than you give
    the graph nodes, an exception will be raised:
    
        >>> n = 5
        >>> g = random_graph(n + 1, weight=(i for i in range(n)))
        Traceback (most recent call last):
          File "<stdin>", line 1, in ?
        Exception: Ran out of iterations for the generator given by 'weight'
    """
    r = random.Random()
    G = networkx.Graph()

    if hasattr(degree, '__getitem__'):
        if len(degree) is not 2:
            raise ValueError('Wrong number of values for (min, max) degree')
        degree = r.randint(*degree)

    for key in properties:                  
        if hasattr(properties[key], '__call__'):
            check_value = properties[key](r)
            if hasattr(check_value, 'next'):
                properties[key] = check_value

    for n in range(degree):
        new_node = base_class()
        
        G.add_node(new_node)
            
        for key in properties:
            property_key = str(key)
            property_value = properties[key]
            
            # Avoid overwriting properties.  This could happen if the
            # user passes in something that is a dictionary rather
            # than a traditional KV list.  We'll accept anything that
            # has __str__, but __str__ is not meant to be unique.
            if hasattr(new_node, property_key): 
                raise Exception('Did not overwrite duplicate property')
            
            new_value = None
              
            if hasattr(property_value, '__call__'):
                new_value = property_value(r)
            elif hasattr(property_value, 'next'):
                try:
                    new_value = next(property_value)
                except StopIteration:
                    raise Exception('Ran out of iterations for the generator given by {!r}'\
                                        .format(property_key))
            elif '(' in property_value and ')' in property_value: # val is a func
                # collect the arguments
                # TODO: make this safe, i.e. destroy `eval`
                func = property_value[:property_value.index('(')]
                args = eval(property_value[property_value.index('('):])
                ex = lambda t: ValueError('Wrong number of arguments for {}.'.format(t))
                
                if func == 'float':
                    if len(args) is not 0: raise ex('float')
                    new_value = r.random()
                elif func == 'int':
                    if len(args) is not 2: raise ex('int')
                    new_value = r.randint(*args)
                elif func == 'bool':
                    new_value = r.random() <= float(args)
            else:
                new_value = property_value
            
            G.node[new_node][property_key] = new_value

    for src, dst in combinations(G.nodes(), 2):
        # perhaps add switch to check for __call__(node_a, node_b)
        if r.random() <= edge_probability:
            G.add_edge(src, dst)
    
    return G

if __name__ == '__main__':
    import doctest
    doctest.testmod()
