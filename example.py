
import networkx as nx
import tkinter as tk
from odin import *

def new_graph():
    grapher.set_graph(Generators.sparse_graph(10, marked='bool(.5)'))
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

grapher = Grapher(root, width=400, height=300, background='gray')
grapher.pack()
grapher.set_layout_algorithm(nx.circular_layout)
grapher.set_node_painter(marked_node_painter)

new_graph()

tk.Button(root, text='New Graph', command=new_graph).pack()
