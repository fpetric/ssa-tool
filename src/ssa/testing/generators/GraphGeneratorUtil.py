
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
    generator.  If the value does not have __call__ defined, it will
    be assumed a string unless, as a string, it is one of the following:

    - 'int(n,m)': a random integer in [n, m]
    - 'float()' : a random floating point number in [0, 1)
    - 'bool(n)' : a random boolean with a probability of truth between
                  0 and 1 inclusive (where 1 is True).

    If the property value is neither callable nor a string of this
    form, then the value is simply set raw.

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

    >>> all(map(lambda n: n.marked,
    ...         random_graph(1000, marked='bool(1)')))
    True
    >>> any(map(lambda n: n.marked,
    ...         random_graph(1000, marked='bool(0)')))
    False

    float():

    >>> .45 < sum(map(lambda n: n.weight,
    ...         random_graph(1000, weight='float()')))/1000 < .55
    True

    and int(min, max):

    >>> all(map(lambda n: n.age in range(40, 50 + 1),
    ...         random_graph(1000, age='int(40, 50)')))
    True

    Be careful about the arguments you pass.  If you want a range of
    possible values for the degree, ensure you pass an iterable of
    exactly two elements:

    >>> random_graph((1,2,3))
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    Exception: Wrong number of values for (min, max) degree

    Mind the arguments for the keywords 'bool', 'int', and 'float'.

    >>> random_graph(5, marked='int(3,4,5)')
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    Exception: Wrong number of arguments for int.
    """
    r = random.Random()
    G = networkx.Graph()

    if hasattr(degree, '__getitem__'):
        if len(degree) is not 2:
            raise Exception('Wrong number of values for (min, max) degree')
        degree = r.randint(*degree)

    for n in range(degree):
        new_node = base_class()

        for key in properties:
            new_prop = str(key)
            new_value = properties[key]
            # Avoid overwriting properties.  This could happen if the
            # user passes in something that is a dictionary rather
            # than a traditional KV list.  We'll accept anything that
            # has __str__, but __str__ is not meant to be unique.
            if hasattr(new_node, new_prop): 
                raise Exception('Did not overwrite duplicate property')

            if hasattr(properties[key], '__call__'):
                setattr(new_node, new_prop, new_value(r))
            else:
                if '(' in new_value and ')' in new_value: # val is a func
                    # collect the arguments
                    # TODO: make this safe, i.e. destroy `eval`
                    func = new_value[:new_value.index('(')]
                    args = eval(new_value[new_value.index('('):])
                    ex = lambda t: Exception('Wrong number of arguments for {}.'.format(t))

                    if func == 'float':
                        if len(args) is not 0: raise ex('float')
                        new_value = r.random()
                    elif func == 'int':
                        if len(args) is not 2: raise ex('int')
                        new_value = r.randint(*args)
                    elif func == 'bool':
                        new_value = r.random() <= float(args)

                setattr(new_node, new_prop, new_value)
        
        G.add_node(new_node)

    for src, dst in combinations(G.nodes(), 2):
        # perhaps add switch to check for __call__(node_a, node_b)
        if r.random() <= edge_probability:
            G.add_edge(src, dst)
    
    return G

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import sys

    if 'unittests' in sys.argv:
        from collections import Counter
        import  sys
        print 'Running unit test on `random_graph`:'
        print '  Creating a random graph with attributes:'
        print '              degree = 1000'
        print '    edge probability = 0.7'
        print '          base class = BasicNode'
        print '              marked = bool(.3)'
        print '              answer = lambda r: r.choice(["yes", "no", "maybe"])'
        print '                 age = int(18, 65)'
        print '              weight = float()'
        print '  please be patient...',
        sys.stdout.flush()
        G = random_graph(1000, .7, marked='bool(.3)',
                                  answer=lambda r: r.choice(['yes', 'no', 'maybe']),
                                  weight='float()',
                                  age='int(18, 65)')
        print 'Graph created.  Calculating statistics...'
        sys.stdout.flush()

        ll=lambda attr: map(lambda n: getattr(n, attr), G.nodes())
        stats = {}
        stats['marked'] = float(sum(ll('marked')))/len(G.nodes())
        stats['answer'] = Counter(ll('answer'))
        stats['weight'] = float(sum(ll('weight')))/len(G.nodes())
        stats['age']    = float(sum(ll('age')))/len(G.nodes())

        print '  Stats:'
        print '    Probability of truth: {marked}'.format(**stats)
        print '            Answer stats: yes={answer[yes]:>3} no={answer[no]:>3} maybe={answer[maybe]:>3}'.format(**stats)
        print '             Average age: {age}'.format(**stats)
        print '          Average weight: {weight}'.format(**stats)
        # TODO: make sure the results are within bounds
        print 'Unit test of `random_graph` complete.'
