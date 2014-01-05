
import pygame
import networkx as nx

from ColorBank import ColorBank
from BasicNode import BasicNode

class Visualizer:
    def __init__(self, size=(640, 480), graph=nx.Graph()):
        """where `size` is a 2-tuple representing screen dimens"""

        self.screen = pygame.display.set_mode(size)

        self.colors = ColorBank()
        self.graph = graph
        self.layout_algorithms = [getattr(nx, a) for a in dir(nx) if a.endswith('_layout')]
        # TODO sometimes crashes here; why?
        self.text_font = pygame.font.SysFont('monospace', 15)

    def do_layout(self, layout_algorithm=None):
        if layout_algorithm is None:
            layout_algorithm = self.layout_algorithms[0]

        try:
            p = layout_algorithm(self.graph)
        except:
            print 'Layout algorithm `{!s}` not yet supported.'.format(repr(layout_algorithm).split()[1])
            print 'Please install the appropriate package.'
            return

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

if __name__ == '__main__':
    pygame.init()
    screen_size = (640, 480)

    import generators

    g = generators.random_graph((5, 20), .3,
                                data='(random)',
                                color=lambda r: ColorBank.random(r),
                                radius='int(3, 10)',
                                position=lambda r: tuple([r.random(), r.random()]))

    vis = Visualizer(size=screen_size, graph=g)
    vis.do_layout()

    vis.loop()
