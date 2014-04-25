
import tkinter as tk
import networkx as nx
from odin import *

def on_reconfigure(event):
    grapher.paint(do_layout=not bool(grapher.layout))

def new_graph():
    global n
    n += 1
    grapher.set_graph(Generators.sparse_graph(n, marked='bool(.25)'))
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
