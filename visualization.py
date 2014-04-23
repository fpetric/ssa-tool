
import tkinter as tk

class Grapher(tk.Canvas):
    def __init__(self, master,
                 graph            = None,
                 layout_algorithm = None,
                 node_painter     = None,
                 edge_painter     = None, *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)

        if layout_algorithm is None:
            layout_algorithm = lambda G: \
                               {n: (0, 0) for n in G.nodes()}
        if node_painter is None:
            node_painter = Grapher.plain_node_painter
        if edge_painter is None:
            edge_painter = Grapher.plain_edge_painter
        self.set_graph(graph)
        self.set_layout_algorithm(layout_algorithm)
        self.set_node_painter(node_painter)
        self.set_edge_painter(edge_painter)

    def paint(self, padx=15, pady=15, do_layout=True):
        if self.graph is None:
            raise Exception('No graph specified.')
        if do_layout and self.layout_algorithm is None:
            raise Exception('No layout algorithm specified.')
        if not do_layout and self.layout is None:
            raise Exception('Re-layout prohibited and no existing layout in place.')
        if not callable(self.layout_algorithm):
            raise Exception('Layout algorithm must be callable.')
        self.delete(tk.ALL)
        wd = self.winfo_width()
        dp = self.winfo_height()
        if do_layout:
            self.layout = self.layout_algorithm(self.graph)
        
        normalized_layout = {node: (self.layout[node][0] * (wd - 2*padx) + padx,
                                    self.layout[node][1] * (dp - 2*pady) + pady)
                             for node in self.layout}
        for edge in self.graph.edges():
            self.paint_edge(normalized_layout, self.graph, *edge)
        for node in self.graph.nodes():
            self.paint_node(normalized_layout, self.graph, node)

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

import networkx as nx
import generators as gn

def on_reconfigure(event):
    grapher.paint(do_layout=not bool(grapher.layout))

def new_graph():
    global n
    n += 1
    grapher.set_graph(gn.sparse_graph(n, marked='bool(.25)'))
    grapher.paint()

n = 5

root = tk.Tk()
grapher = Grapher(root,
                  layout_algorithm=nx.circular_layout,
                  node_painter=Grapher.circle_node_painter,
                  background='#dddddd')
tk.Button(root, text='New Graph', command=new_graph).pack()

grapher.pack(fill = 'both', expand = True)

root.bind('<Configure>', on_reconfigure)

new_graph()

root.mainloop()
exit()

import threading
import collections

class GraphAnimator(Grapher):
    def __init__(self, master, interval=1, *args, **kwargs):
        Grapher.__init__(self, master, *args, **kwargs)
        self.interval = interval

    def load(self, queue):
        self.queue.extend(queue)
    def isdelta(self, change):
        return isinstance(change, dict) and 'new node' in change
    def _queue_next_graph(self):
        change = self.queue.popleft()
        if self.isdelta(change):
            node = change['new node'][0]
            data = change['new node'][1]
            for key, value in data.keys(), data.values():
                self.graph[node][key] = value
        else:
            self.set_graph(change)
    def stop(self):
        self.should_stop = True
    def start(self):
        if not self.should_stop:
            self.paint(self.next_graph, do_layout=False)
            threading.Timer(self.interval, self.start, [self]).start()
            self._queue_next_graph()
