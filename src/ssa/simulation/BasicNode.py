
from ColorBank import ColorBank

class BasicNode:
    default_radius = 25
    default_color = (0,0,0)
    default_data = None
    default_position = (0, 0)

    def __init__(self, position=None,
                       radius=None,
                       color=None,
                       data=None,
                       randomize=None):
        if randomize is not None:
            r=randomize
            if data         is None: data       = '(random)'
            if color        is None: color      = ColorBank.random(r)
            if radius       is None: radius     = r.randint(3,50)
            if position     is None: position   = (r.random(), r.random())
        else:
            if data         is None: data       = BasicNode.default_data
            if color        is None: color      = BasicNode.default_color
            if radius       is None: radius     = BasicNode.default_radius
            if position     is None: position   = BasicNode.default_position

        if any(map(lambda c: not (0 <= c <= 1), position)):
            raise Exception('Woah there buddy.')

        self.data       = data
        self.color      = color
        self.radius     = radius
        self.position   = position
    def __str__(self):
        return str(self.data)
    def __repr__(self):
        return str(self.__dict__)
