
import networkx as nx
import copy
class AnimatedGraph:
    class Delta:
        def __init__(self, changes, actor=None):
            self.changes = changes
            self.actor = actor # the thing that brought about this delta
            """
            changes =>
            { 1: {'marked': True},
              3: {'marked': False} }
            """
        def apply_to(self, graph):
            assert all(lambda n: n in graph,
                       self.changes.keys())
            for node, properties in self.changes.items():
                for key, value in properties.items():
                    graph.node[node][key] = value
    def __init__(self, graph, *deltas):
        self.base_graph = copy.deepcopy(graph)
        self.deltas = list(deltas)
    def __iter__(self):
        graph = self.base()
        yield graph
        for delta in self.deltas:
            delta.apply_to(graph)
            yield graph
    def __getitem__(self, idx):
        current = 0
        track = iter(self)
        G = next(track)
        while current != idx:
            G = next(track)
            current += 1
        return G if G else self.base()
    def __len__(self):
        return len(self.deltas)
    def base(self):
        return copy.deepcopy(self.base_graph)
    def __add__(self, other):
        assert other.base_graph == self.base_graph
        return AnimatedGraph(graph=self.base_graph,
                             deltas=self.deltas.extend(other.deltas))
import random
import itertools
import types
class Generators:
    @staticmethod
    def random_graph(degree, edge_probability=0.5, factory=None, **properties):
        """Generates a random graph of `degree` nodes, a specified
        probability for edges, and a number of random properties.
        
        If `degree` is a tuple, it is assumed to be a (min, max) tuple
        defining an inclusive range of possible degrees.
          
        Each `properties` value can be a function of a random number
        generator.  If the value does not have `__call__` defined, it will be
        assumed a string unless, as a string, it is one of the following:
          
        - 'int(n,m)' :: a random integer in [n, m]
        - 'float()'  :: a random floating point number in [0, 1)
        - 'bool(n)'  :: a random boolean with a probability of truth between 0
                        and 1 inclusive (where 1 is True).
          
        If the property value is neither callable nor a string of this form,
        then the value is simply set raw.
        
        
        """
        r = random.Random()
        G = nx.Graph()
        if factory is None:
            def naturals():
                i = 0
                while True:
                    yield i
                    i += 1
            factory = naturals()
        assert hasattr(factory, '__next__')
        if hasattr(degree, '__getitem__'):
            if len(degree) is not 2:
                raise ValueError('Wrong number of values for (min, max) degree')
            degree = r.randint(*degree)
        for key in properties:                  
            if hasattr(properties[key], '__call__'):
                check_value = properties[key](r)
                if isinstance(check_value, types.GeneratorType):
                    properties[key] = check_value
        for n in range(degree):
            new_node = next(factory)
            G.add_node(new_node)
            for key in properties:
                property_key = str(key)
                property_value = properties[key]
                # Avoid overwriting properties.  This could happen if the
                # user passes in something that is a dictionary rather
                # than a traditional KV list.  We'll accept anything that
                # has __str__, but __str__ is not meant to be unique.
                if hasattr(new_node, property_key): 
                    raise Exception('Did not overwrite duplicate property')
                new_value = None
                if hasattr(property_value, '__call__'):
                    new_value = property_value(r)
                elif isinstance(property_value, types.GeneratorType):
                    try:
                        new_value = next(property_value)
                    except StopIteration:
                        raise Exception('Ran out of iterations for the generator given by {!r}'\
                                            .format(property_key))
                elif '(' in property_value and ')' in property_value: # val is a func
                    func = property_value[:property_value.index('(')]
                    args = eval(property_value[property_value.index('('):])
                    ex = lambda t: ValueError('Wrong number of arguments for {}.'.format(t))
                    if func == 'float':
                        if len(args) is not 0: raise ex('float')
                        new_value = r.random()
                    elif func == 'int':
                        if len(args) is not 2: raise ex('int')
                        new_value = r.randint(*args)
                    elif func == 'bool':
                        new_value = r.random() <= float(args)
                else:
                    new_value = property_value
                G.node[new_node][property_key] = new_value
        for src, dst in itertools.combinations(G.nodes(), 2):
            if r.random() <= edge_probability:
                G.add_edge(src, dst)
        return G
    @staticmethod
    def sparse_graph(degree, extra_paths=None, factory=None, **properties):
        G = Generators.deep_tree(degree=degree, factory=factory, **properties)
        if extra_paths is None:
            extra_paths = int(degree * 1.5)
        for i in range(extra_paths):
            to_connect = random.sample(G.nodes(), 2)
            G.add_edge(*to_connect)
        return G
    @staticmethod
    def broad_tree(degree, factory=None, breadth_factor=.5, **properties):
        G = random_graph(degree=degree, edge_probability=0, factory=factory, **properties)
        while not nx.is_connected(G):
            nodes = G.nodes()
            root = random.choice(nodes)
            nodes.remove(root)
            children = list()
            while nodes:
                n = nodes.pop()
                if random.random() > breadth_factor:
                    children.push(n)
            to_connect = random.sample(nx.connected_components(G), 2)
            u = random.choice(to_connect[0])
            v = random.choice(to_connect[1])
            G.add_edge(u, v)
        return G
    @staticmethod
    def deep_tree(degree, factory=None, **properties):
        G = Generators.random_graph(degree=degree, edge_probability=0, factory=factory, **properties)
        while not nx.is_connected(G):
            to_connect = random.sample(nx.connected_components(G), 2)
            u = random.choice(to_connect[0])
            v = random.choice(to_connect[1])
            G.add_edge(u, v)
        return G
def neighbor_data(graph, node):
    return {v: graph.node[v]
            for v in graph.neighbors(node)}
import yaml
class SelectiveYAMLObject(yaml.YAMLObject):
    hidden_fields = []
    @classmethod
    def to_yaml(cls, dumper, data):
        new_data = copy.deepcopy(data)
        for item in cls.hidden_fields:
            del new_data.__dict__[item]
        return dumper.represent_yaml_object(
            cls.yaml_tag, new_data,
            cls, flow_style=cls.yaml_flow_style)
class Bundle:
    def __init__(self, initpath=None,
                 move_dir='moves', predicate_dir='predicates',
                 description_document='bundle.yaml'):

        self.entities             = set()
        self.move_dir             = move_dir
        self.predicate_dir        = predicate_dir
        self.description_document = description_document

        self.__len__      = self.entities.__len__
        self.__contains__ = self.entities.__contains__
        self.__iter__     = lambda s: iter(s.entities)
        self.__next__     = iter(self.entities).__next__

        if initpath is not None:
            self.load(initpath)

    def __len__(self):
        return len(self.entities)

    def __contains__(self, item):
        return self.entities.contains(item)

    def __iter__(self):
        self.__entity_iterator = iter(self.entities)
        return self.__entity_iterator

    def __next__(self):
        r = next(self.__entity_iterator)

    def load(self, path):
        fullpath = '{!s}/{!s}'.format(path, self.description_document)
        yaml_objects = list(yaml.load_all(open(fullpath, 'r')))
        [self.load_definition(path, obj) for obj in yaml_objects]
        for algorithm in yaml_objects:
            if hasattr(algorithm, 'resolve_rules'):
                algorithm.resolve_rules(yaml_objects)
        self.entities.update(yaml_objects)

    def load_definition(self, path, ssa_obj):
        if hasattr(ssa_obj, 'filename'):
            tag   = ssa_obj.__class__.yaml_tag
            style = ssa_obj.__class__.yaml_flow_style

            # Create new class with inherited YAML attributes
            ssa_obj.__class__ = type(ssa_obj.__class__.__name__,
                                     (ssa_obj.__class__,),
                                     {
                                         'yaml_tag': tag,
                                         'yaml_flow_style': style
                                     })

            # Define call
            with open('/'.join([path, ssa_obj.ssa_folder, ssa_obj.filename])) as f:
                lines = f.readlines()

            ssa_obj.definition = lines

            lines = ['def temp(self, v, N):\n'] + \
                    ['    ' + l for l in lines]
            exec("".join(lines), locals())
            ssa_obj.__class__.__call__ = locals()['temp']


    def sorted(self):
        return sorted(self.entities, reverse=True, key=lambda e: repr(e))

    def to_yaml(self):
        return yaml.dump_all(self.sorted(), explicit_start=True)

    def dump(self, path):
        # create path as directory
        import os
        os.makedirs(path, exist_ok=True)
        for subdir in [self.move_dir, self.predicate_dir]:
            os.makedirs('{!s}/{!s}'.format(path, subdir), exist_ok=True)
        # gather predicates and moves and set in directories
        predicates = []
        moves      = []
        algorithms = []
        for entity in self.entities:
            name = entity.__class__.__name__
            if   name ==      Move.__name__:      moves.append(entity)
            elif name == Predicate.__name__: predicates.append(entity)
            elif name == Algorithm.__name__: algorithms.append(entity)
            else: raise Exception('Encountered an invalid object: {!r}'.format(name))

        for p in predicates:
            with open('/'.join([path, self.predicate_dir, p.filename]), 'w') as f:
                f.writelines(p.definition)

        for p in moves:
            with open('/'.join([path, self.move_dir, p.filename]), 'w') as f:
                f.writelines(p.definition)

        for a in algorithms:
            a.simplify()

        yaml.dump_all(self.sorted(),
                      open('{}/{}'.format(path, self.description_document), 'w'),
                      explicit_start=True)

        for a in algorithms:
            a.resolve_rules(self.entities)

    def types(self, cls):
        for entity in self.entities:
            if isinstance(entity, cls):
                yield entity
    def lookup(self, cls, name):
        hits = list()
        for entity in self.types(cls):
            if entity.name == name:
                hits.append(entity)
        if not hits:
            return None
        elif len(hits) > 1:
            raise Exception('multiply defined names for {}."{}"'.format(cls.__name__, name))
        else:
            return hits[0]
class Predicate(SelectiveYAMLObject):
    yaml_tag = u'!Predicate'
    ssa_folder = 'predicates'
    yaml_flow_style = False
    hidden_fields=['definition', '_run_func']
    
    def __init__(self, name, filename, description=None, author=None, date=None, tex=None):
        self.filename    = filename
        self.name        = name
        self.description = description
        self.author      = author
        self.date        = date
        self.tex         = tex
    
    def __repr__(self):
        return "{!s} '{!s}'".format(self.__class__.__name__.lower(), self.name)
    
    def __call__(self, vertex, neighborhood):
        assert hasattr(self, '_run_func') and self._run_func
        return self._run_func(vertex, neighborhood)

class Move(SelectiveYAMLObject):
    yaml_tag = u'!Move'
    ssa_folder = 'moves'
    yaml_flow_style = False
    hidden_fields=['definition', '_run_func']
    
    def __init__(self, name, filename, description=None, author=None, date=None, tex=None):
        self.filename    = filename
        self.name        = name
        self.description = description
        self.author      = author
        self.date        = date
        self.tex         = tex
    
    def __repr__(self):
        return "{!s} '{!s}'".format(self.__class__.__name__.lower(), self.name)
    
    def __call__(self, vertex, neighborhood):
        assert hasattr(self, '_run_func') and self._run_func
        return self._run_func(vertex, neighborhood)


class Rule(yaml.YAMLObject):
    yaml_tag = u'!Rule'
    def __init__(self, predicate=None, moves=None, name=None, description=None, author=None, date=None):
        self.description = description
        self.author      = author
        self.date        = date
        self.predicate   = predicate
        self.moves       = moves
        self.name        = name

    def __repr__(self):
        return "rule '{!s}'".format(self.name)

    def applies_to(self, v, N):
        return bool(self.predicate(v, N))

    def apply_to(self, graph, node, r=random):
        move = r.choice(self.moves)

        move(graph.node[node], neighbor_data(graph, node))

        return Delta(changes={node: neighbor_data(graph, node)},
                     actor=move)
class Algorithm(yaml.YAMLObject):
    yaml_tag = u'!Algorithm'
    yaml_flow_style = False
    ssa_folder = None

    def __init__(self, name=None, author=None, date=None, rules=None):
        self.name   = name
        self.author = author
        self.date   = date
        self.rules  = rules

    def resolve_rules(self, entities):
        mapping = {entity.name if hasattr(entity, 'name') else repr(entity): entity
                   for entity in entities}
        for rule in self.rules:
            rule.predicate = mapping[rule.predicate]
            rule.moves = [mapping[m] for m in rule.moves]
    def simplify(self):
        '''undoes resolve_rules for saving'''
        for rule in self.rules:
            rule.predicate = rule.predicate.name
            rule.moves = [m.name for m in rule.moves]

    def run(self, graph, count=1):
        assert count >= 0
        anigraph = AnimatedGraph(graph)
        while count > 0:
            privileged_nodes = dict()
            for node in graph:
                neighbors = neighbor_data(graph, node)
                for rule in self.rules:
                    if rule.applies_to(graph.node[node], neighbors.values()):
                        if node in privileged_nodes:
                            privileged_nodes[node] += rule
                        else:
                            privileged_nodes[node] = [rule]
            if not privileged_nodes:
                break
            node = random.choice(list(privileged_nodes.keys()))
            neighbors = neighbor_data(graph, node)
            applied_rule = random.choice(privileged_nodes[node])
            delta = rule.apply_to(graph, node)
            anigraph.deltas.append(delta)
            count -= 1
        return anigraph

    def has_stabilized(self, graph):
        for node in graph:
            neighbors = neighbor_data(graph, node)
            for rule in self.rules:
                if rule.applies_to(graph.node[node], neighbors.values()):
                    return False
        return True

    def stabilize(self, graph):
        while not self.has_stabilized(graph):
            self.run(graph)

    def __repr__(self):
        return "{!s} '{!s}'".format(self.__class__.__name__.lower(), self.name)

    def lookup(self, name):
        for rule in self.rules:
            if rule.name == name:
                return rule
pass # cli
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
def gui():
    import ttk
    root = tk.Tk()
    root.title('SSA Graphical Aggregator and Tester')

    def add_new(widget_dictionary, name, pre=None, post=None):
        """Adds a new item"""
        def f(entity = None):
            if pre: pre()
            widget_dictionary[name][1].insert(END, '<name>')
            if post: post()
        return f
    def del_sel(widget_dictionary, name, pre=None, post=None):
        """Deletes the selected item"""
        def f():
            if pre: pre()
            widget_dictionary[name][1].delete(ACTIVE)
            if post: post()
        return f
    def name_updater(widget_dictionary, variable_dictionary, listbox, variable, data):
        def update_name_according_to_variable():
            new_name = variable_dictionary[variable].get()
            if new_name != variable_dictionary[data].name:
                variable_dictionary[data].name = new_name
                w = get(widget_dictionary, listbox)
                i = w.curselection()
                w.delete(i)
                w.insert(i, new_name)
                w.activate(i)
                w.selection_set(i)
        return update_name_according_to_variable
    def Construct_PM_Tab(cls, w, v, f):
        v['current'] = None
        v['name']        = StringVar(root)
        v['file']        = StringVar(root)
        v['author']      = StringVar(root)
        v['date']        = StringVar(root)
        v['description'] = StringVar(root)
        v['tex']         = StringVar(root)
        v['name'].trace('w', lambda n, i, m: f['update name']())
        v['file'].trace('w', lambda n, i, m: f['sanitize file']())
        def scr2bdl():
            if not v['current']:
                return
            from datetime import datetime
            v['current'].name        = v['name'].get()
            v['current'].author      = v['author'].get()
            v['current'].date        = datetime.strptime(v['date'].get(), '%Y-%m-%d')
            v['current'].filename    = v['file'].get()
            v['current'].description = v['description'].get()
            v['current'].tex         = v['tex'].get()
            v['current'].definition  = [l+'\n' for l in w['definition'][1].get(1.0, END).split('\n')[:-2]]
        f['screen to bundle'] = scr2bdl
        def bdl2scr():
            v['name'        ].set(v['current'].name)
            v['author'      ].set(v['current'].author)
            v['file'        ].set(v['current'].filename)
            v['description' ].set(v['current'].description)
            v['tex'         ].set(v['current'].tex)
            if hasattr(v['current'].date, 'date'):
                v['date'        ].set(v['current'].date.date())
            else:
                v['date'        ].set(v['current'].date)
            try:
                w['definition'][1].delete(1.0, END)
            except:
                pass
            w['definition'  ][1].insert(1.0, ''.join(v['current'].definition))
            w['definition'  ][1].do_hl()
        f['bundle to screen'] = bdl2scr
        def clrscr():
            v['name'        ].set('')
            v['author'      ].set('')
            v['date'        ].set('')
            v['file'        ].set('')
            v['description' ].set('')
            v['tex'         ].set('')
            try:
                w['definition'  ][1].delete(1.0, END)
            except:
                pass
        f['clear screen'] = clrscr
        def update_name():
            new_name = v['name'].get()
            if new_name != v['current'].name:
                # BUG: crashes if a word is deleted (as opposed to a single character)
                v['current'].name = new_name
                widget = w['list'][1]
                idx = widget.curselection()
                widget.delete(idx)
                widget.insert(idx, new_name)
                widget.activate(idx)
                widget.selection_set(idx)
        f['update name'] = update_name
        def sanitize_file():
            old = v['file'].get()
            new = old.replace(' ', '-') + ('.py' if not old.endswith('.py') else '')
            v['file'].set(new)
        f['sanitize file'] = sanitize_file
        def sel_new(event):
            f['screen to bundle']()
            widget = w['list'][1]
            selected = widget.get(w.curselection())
            v['current'] = bundle.lookup(cls, selected)
            
            if not v['current']:        # a new entity was made
                v['current'] = cls()
                for attr in ['name', 'author', 'date', 'description', 'filename', 'tex', 'definition']:
                    setattr(v['current'], attr, '<%s>' % attr)
                v['current'].date = '2014-01-01'
                bundle.entities.add(v['current'])
            
            f['bundle to screen']()
        f['on select new'] = sel_new
        f['add']              = add_new(w, 'list', cls)
        f['remove']           = del_sel(w, 'list')
        w['tab']         = None ,        Frame(top)
        w['list']        = (0   ,   0) , new(Listbox,    w, 'tab' , height = 18)
        w['name']        = (180 ,   0) , new(Entry,      w, 'tab' , textvariable = v['name'])
        w['author']      = (360 ,   0) , new(Entry,      w, 'tab' , textvariable = v['author'])
        w['date']        = (180 ,  25) , new(Entry,      w, 'tab' , textvariable = v['date'])
        w['file']        = (360 ,  50) , new(Entry,      w, 'tab' , textvariable = v['file'])
        w['description'] = (180 ,  50) , new(Entry,      w, 'tab' , textvariable = v['description'])
        w['tex']         = (360 ,  25) , new(Entry,      w, 'tab' , textvariable = v['tex'])
        w['add']         = (0   , 310) , new(Button,     w, 'tab' , text = 'add'    , command = f['add'])
        w['remove']      = (80  , 310) , new(Button,     w, 'tab' , text = 'remove' , command = f['remove'])
        w['definition']  = (180 ,  80) , new(SourceText, w, 'tab' , width = 80, height = 16)
        bind(w, 'list', '<'+'<ListboxSelect>>', f['on select new'])
    Construct_PM_Tab(Predicate, pdw, pdv, pdf)
    Construct_PM_Tab(Move     , mvw, mvv, mvf)
    

    root.mainloop()
# Local Variables:
# python-shell-interpreter: "python3"
# truncate-lines: t
# End:
