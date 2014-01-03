
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

    Each `properties` value can be a function of a random number
    generator.  If the value does not have __call__ defined, it will
    be assumed a string unless, as a string, it is one of the following:

    - 'int(n,m)': a random integer in [n, m]
    - 'float()' : a random floating point number in [0, 1)
    - 'bool(n)': a random boolean with a probability of truth between
                 0 and 1 inclusive.

    If the property value is neither callable nor a string of this
    form, then the value is simply set raw.
    """
    r = random.Random()
    G = networkx.Graph()

    for n in range(degree):
        new_node = base_class()

        for key in properties:
            new_prop = str(key)
            new_value = properties[key]
            # Avoid overwriting properties.  This could happen if the
            # user passes in something that is a dictionary rather
            # than a tradition KV list.  We'll accept anything that
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
    from collections import Counter
    print 'Running unit test on `random_graph`:'
    print '  Creating a random graph with attributes:'
    print '              degree = 1000'
    print '    edge probability = 0.7'
    print '          base class = BasicNode'
    print '              marked = bool(.3)'
    print '              answer = lambda r: r.choice(["yes", "no", "maybe"])'
    print '                 age = int(18,65)'
    print '              weight = float()'
    G = random_graph(1000, .7, marked='bool(.3)',
                              answer=lambda r: r.choice(['yes', 'no', 'maybe']),
                              weight='float()',
                              age='int(18,65)')
    print '  Graph created.'
    #for n in G.nodes(): print '    {i}= {0.marked!s:<6} {0.answer:<6} {0.age:>3} {0.weight}'.format(n,i=id(n))
    print '  Stats:'

    ll=lambda attr: map(lambda n: getattr(n, attr), G.nodes())

    print '    Probability of truth:', float(sum(ll('marked')))/len(G.nodes())
    print '            Answer stats: yes={0[yes]:>3} no={0[no]:>3} maybe={0[maybe]:>3}'.format(Counter(ll('answer')))
    print '             Average age:', float(sum(ll('age')))/len(G.nodes())
    print '          Average weight:', float(sum(ll('weight')))/len(G.nodes())
    # TODO: make sure the results are within bounds
    print 'Unit test of `random_graph` complete.'
