
import unittest
from nose.tools import *

from ssa.simulation import *

class RandomGraphTest(unittest.TestCase):
    @classmethod
    def setupClass(cls):
        cls.G = \
        generators.random_graph(\
            1000, .7,
            marked='bool(.3)',
            answer=lambda r: r.choice(['yes', 'no', 'maybe']),
            weight='float()',
            age='int(18, 65)')

    def get_attribute(self, attr):
        return map(lambda n: getattr(n, attr), self.G.nodes())
    
    def avg(self, attr):
        return float(sum(self.get_attribute(attr)))/len(self.G.nodes())

    def test_bool(self):
        assert_almost_equal(self.avg('marked'), .3, 1)
      
    def test_float(self):
        assert_almost_equal(self.avg('weight'), .5, 1)
      
    def test_int(self):
        g = self.avg('age')
        e = (18.0 + 65)/2
      
        assert_almost_equal(g/100, e/100, 1)
      
    def test_func(self):
        g = sum([abs(self.get_attribute('answer').count(c) - 333.33) / 1000.0
                 for c in ['yes', 'no', 'maybe']])
      
        assert_less(g, .1)

    def test_raw_func(self):
        choices = ['yes', 'no', 'maybe']
        def get_marked(random_instance):
            return random_instance.choice(choices)
        g = generators.random_graph(15, marked=get_marked)
        assert all(map(lambda n: n.marked in choices, g.nodes()))
    
    def test_lambda_func(self):
        choices = ['yes', 'no', 'maybe']
        g = generators.random_graph(15, marked=lambda r: r.choice(choices))
        assert all(map(lambda n: n.marked in choices, g.nodes()))
    def test_generator_func(self):
        def gen_weight(random_instance):
            while True:
                yield random_instance.random()
        g = generators.random_graph(15, weight=gen_weight)
        assert all(map(lambda n: 0 <= n.weight < 1, g.nodes()))
    
    def test_generator_func2(self):
        def gen_in_range(minimum, maximum):
            # iter(int, True) is an infinite generator: 0, 0, 0, ...
            return lambda r: (r.uniform(minimum, maximum)
                              for i in iter(int, True))
    
        g = generators.random_graph(15, weight=gen_in_range(10, 20))
        assert all(map(lambda n: 10 <= n.weight <= 20, g.nodes()))
