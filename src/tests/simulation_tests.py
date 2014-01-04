
import unittest
from nose.tools import *
from ssa.simulation import *

class RandomGraphTest(unittest.TestCase):
    @classmethod
    def setupClass(cls):
        cls.G = generators.random_graph(\
            1000, .7,
            marked='bool(.3)',
            answer=lambda r: r.choice(['yes', 'no', 'maybe']),
            weight='float()',
            age='int(18, 65)')

    def ll(self, attr):
        return map(lambda n: getattr(n, attr), self.G.nodes())

    def avg(self, attr):
        return float(sum(self.ll(attr)))/len(self.G.nodes())

    def test_bool(self):
        assert_almost_equal(self.avg('marked'), .3, 1)

    def test_float(self):
        assert_almost_equal(self.avg('weight'), .5, 1)

    def test_int(self):
        g = self.avg('age')
        e = (18.0 + 65)/2

        assert_almost_equal(g/100, e/100, 1)

    def test_func(self):
        g = sum([abs(self.ll('answer').count(c) - 333.0) / 1000.0
                 for c in ['yes', 'no', 'maybe']])

        assert_less(g, .1)
