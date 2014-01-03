
import pygame
# import pygame.gfxdraw
import networkx as nx

pygame.init()

class ColorBank:
    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red   = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue  = (0, 0, 255)

    def set_color(self, name, red, green, blue):
        setattr(self, str(name), (red, green, blue))

    @classmethod
    def get_inverse(cls, color, alpha=1):
        inverses = [255 - c for c in color] + [alpha]
        return tuple((channel for channel in inverses))

    @classmethod
    def random(cls, r):
        return tuple((r.randint(0, 255) for i in range(3)))

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

class Visualizer:
    def __init__(self, size=(640, 480), graph=nx.Graph()):
        """where `size` is a 2-tuple representing screen dimens"""

        self.screen = pygame.display.set_mode(size)

        self.colors = ColorBank()
        self.graph = graph
        self.layout_algorithms = \
            [
            #nx.circular_layout,
            #nx.fruchterman_reingold_layout,
            #nx.graphviz_layout,
            #nx.pygraphviz_layout,
            #nx.random_layout,
            #nx.shell_layout,
            nx.spectral_layout,
            #nx.spring_layout
            ]
        # TODO sometimes crashes here; why?
        self.text_font = pygame.font.SysFont('monospace', 15)

    def do_layout(self, layout_algorithm=None):
        if layout_algorithm is None:
            layout_algorithm = random.Random().choice(self.layout_algorithms)

        p = layout_algorithm(self.graph)

        for node, position in zip(p.keys(), p.values()): # in p isn't working: iteration over non-sequence
            node.position = ((position[0] + 1) / 2, (position[1] + 1) / 2)

    def draw(self):
        self.screen.fill(self.colors.green)
        size = self.screen.get_size()

        for src, dst in self.graph.edges():
            pygame.draw.line(self.screen, self.colors.white,
                             self.floats_to_pos(src.position),
                             self.floats_to_pos(dst.position), 3)

        for n in self.graph.nodes():
            normal_pos = self.floats_to_pos(n.position) # keep track of z order for drag drop
            pygame.draw.circle(self.screen, n.color, normal_pos, n.radius, 0)
            label = self.text_font.render(str(n.data), True, ColorBank.get_inverse(n.color))
            self.screen.blit(label, normal_pos)

        pygame.display.update()

    def floats_to_pos(self, floats):
        return tuple((int(coordinate * scale) for coordinate, scale in zip(floats, self.screen.get_size())))

    def pos_to_floats(self, position):
        return tuple((coordinate / scale for coordinate, scale in zip(position, self.screen.get_size())))

    def loop(self):
        ingame=True
        while ingame:
            self.draw()
            pygame.time.delay(500)
            self.do_layout()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    ingame = False

import random
r = random.Random()

screen_size = (640, 480)

g = nx.Graph()

for i in range(5):
    g.add_node(BasicNode(data=i, randomize=r))

get_node=lambda i: filter(lambda n: n.data == i, g)

import itertools
for src, dst in itertools.combinations(g.nodes(), 2):
    if r.random() < .75:
        g.add_edge(src, dst)

vis = Visualizer(size=screen_size, graph=g)
vis.do_layout()

vis.loop()
