import tkinter as tk

# TODO can leverage tk.Canvas.postscript in export

class Grapher(tk.Canvas):
    def __init__(self, graph, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.set_graph(graph)

    def set_graph(self, graph):
        """Ensures `graph` is in the appropriate format and stores it"""
        self.graph = graph

    def set_default_layout(self, layout_algorithm):
        assert callable(layout_algorithm)
        self.layout_algorithm = layout_algorithm

    def set_node_painter(self, node_painter):
        pass

    def paint_node_plain(self, layout, node):
        self.create_text((layout[node][0], layout[node][1]), str(node))

    def paint_edge_plain(self, layout, source, sink):
        self.create_line(layout[source][0],    layout[source][1],
                         layout[sink]  [0],    layout[sink]  [1])

    def paint(self, layout=None):
        # clear the screen
        self.delete('all')

        if layout is None:
            layout = self.layout_algorithm
        
        positions = layout(self.graph)
 
        # need to consider such things as zoom?
        normalized_layout = {tree: (scale*positions[tree][0] + xshift,
                                    scale*positions[tree][1] + yshift)
                             for tree in positions}

        for node in graph.nodes():
            self.paint_node(layout, node)
        for edge in graph.edges():
            self.paint_edge(layout, *edge)
 
    @staticmethod
    def draw_tree(tree, layout):
        root_position = layout[tree]
        self.create_text(root_position, text=tree.value)
        for subtree in tree.children:
            # draw subtrees
            self.draw_tree(subtree, layout)
            # draw edges to subtrees
            subtree_position = layout[subtree]
            self.create_line(root_position[0],    root_position[1],
                          subtree_position[0], subtree_position[1])
 
# Local Variables:
# python-shell-interpreter: "python3"
# End:
