
import pygame
import networkx as nx

from ColorBank import ColorBank
from BasicNode import BasicNode

class Visualizer:
    def __init__(self, size=(640, 480), graph=nx.Graph(), edge_width = 2):
        """where `size` is a 2-tuple representing screen dimens"""

        self.screen = pygame.display.set_mode(size)

        self.colors = ColorBank()
        self.graph = graph
        self.edge_width = edge_width
        self.layout_algorithms = [getattr(nx, a) for a in dir(nx) if a.endswith('_layout')]
        # TODO sometimes crashes here; why?
        self.text_font = pygame.font.SysFont('monospace', 15)

    def do_layout(self, layout_algorithm=nx.spring_layout):
        try:
            p = layout_algorithm(self.graph)
        except:
            print 'Layout algorithm `{!s}` not yet supported.'.format(repr(layout_algorithm).split()[1])
            print 'Please install the appropriate package.'
            return

        for node, position in zip(p.keys(), p.values()): # in p isn't working: iteration over non-sequence
            self.graph.node[node]['position'] = ((position[0] + 1) / 2, (position[1] + 1) / 2)

    def draw(self):
        self.screen.fill(self.colors.green)
        size = self.screen.get_size()

        for src, dst in self.graph.edges():
            pygame.draw.line(self.screen, self.colors.white,
                             self.floats_to_pos(self.graph.node[src]['position']),
                             self.floats_to_pos(self.graph.node[dst]['position']), self.edge_width)

        for node, node_data in self.graph.nodes(data=True):
            normal_pos = self.floats_to_pos(node_data['position']) # keep track of z order for drag drop
            pygame.draw.circle(self.screen, node_data['color'], normal_pos, node_data['radius'], 0)
            label = self.text_font.render(str(node_data['data']), True, ColorBank.get_inverse(node_data['color']))
            self.screen.blit(label, normal_pos)

        pygame.display.update()

    def floats_to_pos(self, floats):
        return tuple((int(coordinate * scale) for coordinate, scale in zip(floats, self.screen.get_size())))

    def pos_to_floats(self, position):
        return tuple((coordinate / scale for coordinate, scale in zip(position, self.screen.get_size())))

    def loop(self):
        """Runs the simulator.

        >>> pygame.init()
        (6, 0)
        >>> Visualizer(size=(640, 480), graph=make_graph()).loop()
        """
        ingame=True
        for i in range(3):
            self.graph = make_graph()
            for i in range(50):
                self.do_layout()
                self.draw()
                pygame.time.delay(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    ingame = False
        pygame.quit()

import generators
make_graph = lambda: \
    generators.random_graph((5, 20), .3,
                            data=(i for i in range(50)),
                            color=lambda r: ColorBank.random(r),
                            radius='int(3, 10)',
                            position=lambda r: tuple([r.random(), r.random()]))
  
if __name__ == '__main__':
    import doctest
    doctest.testmod()
