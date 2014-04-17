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
        self.paint_node = lambda layout, graph, node: \
                          node_painter(self, layout, graph, node)

    def set_edge_painter(self, edge_painter):
        self.paint_edge = lambda layout, graph, source, sink: \
                          edge_painter(self, layout, graph, source, sink)

    def paint(self, padx=15, pady=15):
        # clear the screen
        self.delete(tk.ALL)

        if self.layout_algorithm is None:
            raise Exception('No layout algorithm specified.')
        if self.graph is None:
            raise Exception('No graph specified.')
        
        positions = self.layout_algorithm(self.graph)
 
        wd = int(self.cget('width'))  + int(padx * .2) # TODO why
        dp = int(self.cget('height')) + int(pady * 1.2)

        # need to consider such things as zoom?
        normalized_layout = {tree: (positions[tree][0] * (wd - 2*padx) + padx,
                                    positions[tree][1] * (dp - 2*pady) + pady)
                             for tree in positions}

        for edge in self.graph.edges():
            self.paint_edge(normalized_layout, self.graph, *edge)
        for node in self.graph.nodes():
            self.paint_node(normalized_layout, self.graph, node)

    @staticmethod
    def plain_node_painter(canvas, layout, graph, node):
        canvas.create_text((layout[node][0], layout[node][1]), text=str(node))

    @staticmethod
    def plain_edge_painter(canvas, layout, graph, source, sink):
        canvas.create_line(layout[source][0],    layout[source][1],
                           layout[sink]  [0],    layout[sink]  [1],
                           width=1.0)
    @staticmethod
    def circle_node_painter(canvas, layout, graph, node):
        r = 10
        x = layout[node][0]
        y = layout[node][1]
        canvas.create_oval((x-r, y-r, x+r, y+r), fill='white', tags='node')
        canvas.create_text((x, y), text=str(node), tags='node')
 
################################################################################
################################################################################
################################################################################

import networkx   as nx
import generators as gen

def new_graph():
    gen.reset_basic_node_counter()
    grapher.set_graph(gen.sparse_graph(10, marked='bool(.5)'))
    grapher.paint()

def marked_node_painter(canvas, layout, graph, node):
        r = 10
        x = layout[node][0]
        y = layout[node][1]
        canvas.create_oval((x-r, y-r, x+r, y+r),
                           fill='black' if graph.node[node]['marked'] else 'white',
                           tags='node')
        canvas.create_text((x, y), text=str(node),
                           fill='white' if graph.node[node]['marked'] else 'black',
                           tags='node')

root = tk.Tk()

root.title('Graph Painter 4000')

grapher = Grapher(root, width=400, height=400, background='gray')
grapher.pack()
grapher.set_layout_algorithm(nx.circular_layout)
grapher.set_node_painter(marked_node_painter)

new_graph()

# TODO can totally add event handlers for node clicks since the canvas
# is just a collection of items
tk.Button(root, text='New Graph', command=new_graph).pack()
 
# Local Variables:
# python-shell-interpreter: "python3"
# End:
