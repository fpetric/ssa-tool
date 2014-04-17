from pprint import pprint
import tkinter as tk

# TODO can leverage tk.Canvas.postscript in export

# requires numpy
# sudo pip3 install numpy

class Grapher(tk.Canvas):
    def __init__(self, master, graph=None, layout_algorithm=lambda:None,
                 *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)

        self.set_graph(graph)
        self.set_layout_algorithm(layout_algorithm)

        self.set_node_painter(Grapher.plain_node_painter)
        self.set_edge_painter(Grapher.plain_edge_painter)

    def set_graph(self, graph):
        """Ensures `graph` is in the appropriate format and stores it"""
        self.graph = graph

    def set_layout_algorithm(self, layout_algorithm):
        assert callable(layout_algorithm)
        self.layout_algorithm = layout_algorithm

    def set_node_painter(self, node_painter):
        self.paint_node = lambda \
                          layout, node: node_painter(
                              self, layout, node)

    def set_edge_painter(self, edge_painter):
        self.paint_edge = lambda \
                          layout, source, sink: edge_painter(
                              self, layout, source, sink)

    def paint(self, layout=None):
        # clear the screen
        self.delete(tk.ALL)

        if layout is None:
            if self.layout_algorithm is None:
                raise Exception('No layout algorithm specified.')
            layout = self.layout_algorithm
        
        positions = layout(self.graph)
 
        # Tried self.winfo_width/_height, but
        # 'without a geometry manager, this will always return 1'

        wd = 200.0              # TODO
        dp = 200.0
        xpad = 30
        ypad = 30
        # need to consider such things as zoom?
        normalized_layout = {tree: (positions[tree][0] * (wd - 2*xpad) + xpad,
                                    positions[tree][1] * (dp - 2*ypad) + ypad)
                             for tree in positions}

        for edge in self.graph.edges():
            self.paint_edge(normalized_layout, *edge)
        for node in self.graph.nodes():
            self.paint_node(normalized_layout, node)

    @staticmethod
    def plain_node_painter(canvas, layout, node):
        canvas.create_text((layout[node][0], layout[node][1]), text=str(node))

    @staticmethod
    def plain_edge_painter(canvas, layout, source, sink):
        canvas.create_line(layout[source][0],    layout[source][1],
                           layout[sink]  [0],    layout[sink]  [1],
                           width=2.0)
    @staticmethod
    def circle_node_painter(canvas, layout, node):
        r = 10
        x = layout[node][0]
        y = layout[node][1]
        canvas.create_oval((x-r, y-r, x+r, y+r), fill='white')
        canvas.create_text((x, y), text=str(node))
 
################################################################################
################################################################################
################################################################################

import networkx   as nx
import generators as gen

G = gen.random_graph(5)

root = tk.Tk()

root.title('Graph Painter 2000')
root.geometry('640x480+5+5')

grapher = Grapher(root, width=200, height=200)
print(grapher.winfo_width(), grapher.winfo_height())
grapher.pack()

grapher.create_text((50, 50), text='hello world')
grapher.create_line(5, 5, 100, 50)

if isinstance(grapher, Grapher):
    grapher.set_graph(G)
    grapher.set_layout_algorithm(nx.spring_layout)
    grapher.set_node_painter(Grapher.circle_node_painter)
    grapher.paint()

def new_graph(event):
    gen.reset_basic_node_counter()
    grapher.set_graph(gen.random_graph(10))
    grapher.paint()

# TODO can totally add event handlers for node clicks since the canvas
# is just a collection of items
grapher.bind('<Button-1>', new_graph)
 
# Local Variables:
# python-shell-interpreter: "python3"
# End:
