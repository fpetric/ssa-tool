
import inspect
import random
import copy
import yaml
import re
class Algorithm:
    """A self-stabilizing algorithm

    
    """
    #% algorithm %#
    def __init__(self, ruleset=None):
        self.ruleset = ruleset
        self.__getitem__ = self.ruleset.__getitem__
        self.predicates = lambda: list(self.ruleset.keys())
        self.moves = lambda: [m for m in p for p in self.ruleset.values()]
    #% end-algorithm %#

    #% algorithm-ruleset-assertions %#
    def is_valid_function(function):
        return len(inspect.getargspec(function).args) is 2
    #% end-algorithm-ruleset-assertions %#

    
    #% daemon-run %#
    def run(self, graph, count=1):
        """Run the algorithm `count` times.
    
        
        """
        assert count >= 0
    
        history = list()
        while count > 0:
            privileged_nodes = dict()
            #% daemon-find-privileged-nodes %#
            for node in graph:
                neighborhood = Algorithm.neighbor_data(graph, node)
                #% daemon-get-privileges %#
                for predicate in self.ruleset:
                    if predicate(graph.node[node], neighborhood.values()):
                        if node in privileged_nodes:
                            privileged_nodes[node] += predicate
                        else:
                            privileged_nodes[node] = [predicate]
                #% end-daemon-get-privileges %#
            #% end-daemon-find-privileged-nodes %#
            if not privileged_nodes:
                break
            #% daemon-pick-predicate %#
            node = random.choice(list(privileged_nodes.keys()))
            neighborhood = Algorithm.neighbor_data(graph, node)
            satisfied_predicate = random.choice(privileged_nodes[node])
            #% end-daemon-pick-predicate %#
            #% daemon-apply-move %#
            old_node = copy.deepcopy(node)
            old_node_data = copy.deepcopy(graph.node[node])
            old_neighborhood = copy.deepcopy(neighborhood)
            
            next_move = random.choice(self.ruleset[satisfied_predicate])
            next_move(graph.node[node], neighborhood)
            #% end-daemon-apply-move %#
            history.append({
                'chosen node': (old_node, old_node_data),
                'neighborhood of chosen node': old_neighborhood,
                'next move': next_move.__name__,
                'node after move': graph.node[node]
            })
            count -= 1
        return history
    #% end-daemon-run %#
    def has_stabilized(self):
        """Returns True if the graph has stabilized.
    
        This function runs `Algorithm.run` twice."""
        pass
    def stabilize(self, graph):
        while not self.has_stabilized():
            self.run(graph)
    
    @staticmethod
    def neighbor_data(graph, node):
        return {node: graph.node[node] for node in graph.neighbors(node)}
class Bundle:
    _unsanitary_function_name = re.compile(r'''[^A-Za-z_]''')

    def __init__(self, descriptor = 'bundle.yaml',
                       move_dir   = 'moves',
                       pred_dir   = 'predicates'):
        """Takes a path to a directory, potentially non-existent, and creates
        an SSAX-formatted bundle."""

        self.descriptor = descriptor
        self.move_dir = move_dir
        self.pred_dir = pred_dir

        self.algorithms = list()
        self.predicates = list()
        self.moves = list()

    def read(self, path, scope=globals()):
        def load_function(entity):
            ks = set(entity.keys())
            if 'predicate' in ks:
                folder = self.pred_dir
                name = entity['predicate']
            elif 'move' in ks:
                folder = self.move_dir
                name = entity['move']
            else:
                raise Error('not predicate or move?? find a wizard')

            name = sanitize_function_name(name)
            with open('{}/{}/{}'.format(path, folder, entity['file'])) as f:
                lines = f.readlines()
            lines = ['def {}(v, N):\n'.format(name)] + \
                    ['    '+l for l in lines]
            exec "".join(lines) in scope

            f = scope[name]
            f.__dict__.update(entity)

            if 'predicate' in ks:
                self.predicates.append(f)
            elif 'move' in ks:
                self.moves.append(f)
            else:
                raise Error('''not predicate or move? no but seriously,
                               how did this happen? find a wizard''')


        def sanitize_function_name(name):
            return self._unsanitary_function_name.sub('_', name)

        with open('{path}/{self.descriptor}'.format(path=path, self=self)) as f:
            bundle = yaml.load(f)

        algorithm_descriptions = []
        for entity in bundle:
            keyset = set(entity.keys())
            if 'predicate' in keyset or 'move' in keyset:
                load_function(entity)
            elif 'algorithm' in keyset:
                algorithm_descriptions.append(entity)
            else:
                raise IOError('Error in bundle file {!s}.'.format(path),
                              'No entity matches {!r}.'.format(entity))

        for ad in algorithm_descriptions:
            rules = dict()
            for rule in ad['rules']:
                pred = sanitize_function_name(rule['predicate'])
                pred = scope[pred]
                rules[pred] = list()
                for move in rule['moves']:
                    move = sanitize_function_name(move)
                    move = scope[move]
                    rules[pred].append(move)
            alg = Algorithm(rules)
            alg.__dict__.update(ad)
            self.algorithms.append(alg)

    def add(self, entity, kind):
        ls = None
        if   kind == 'predicate': ls = self.predicates
        elif kind == 'move':      ls = self.moves
        elif kind == 'algorithm': ls = self.algorithms
        else: raise Error('Unknown entity.  Did you spell it right?')
            
    def write(self, path):
        lines = list()
        for entity in self.predicates + self.moves:
            lines.append(yaml.dump(entity.__dict__))

        for a in self.algorithms:
            temp = dict()
            temp
