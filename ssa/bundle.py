# from __future__ import annotations  --  3.7 *only*; lets us return a Bundle from Bundle.create; https://stackoverflow.com/a/33533514/1443496
import yaml
import os
from . import core
from pprint import pprint
from typing import List, Optional
from collections import OrderedDict
import logging

def _yaml_represent_OrderedDict(dumper: yaml.Dumper, data: OrderedDict):
    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map',
        [(dumper.represent_data(k), dumper.represent_data(v))
            for k, v in data.items()])

yaml.add_representer(OrderedDict, _yaml_represent_OrderedDict)

class Bundle(OrderedDict):
    YAML_DUMP_ARGS = {
        'default_flow_style': False,
    }

    BUNDLE_DEFINITION_FILE = 'bundle.yaml'
    MOVES_DIR = 'move'
    PREDS_DIR = 'predicate'

    _path: Optional[str]
    _bundle_file: Optional[str]

    def __init__(self, path: Optional[str] = None) -> None:
        self.set_path(path)
    def set_path(self, path: Optional[str]) -> None:
        """Set the file path of this bundle.

        By convention, this path should end in '.ssax'.

        """
        self._path = path
        if path:
            self._bundle_file = os.path.join(path, Bundle.BUNDLE_DEFINITION_FILE)

    @staticmethod
    def exists(path: str) -> bool:
        """Test if path describes an existing bundle."""
        return os.path.isdir(path) and os.path.isfile(os.path.join(path, Bundle.BUNDLE_DEFINITION_FILE))

    @staticmethod
    def create(path: str) -> 'Bundle':
        """Create a new bundle at a given path."""
        if Bundle.exists(path):
            raise os.error("bundle exists")
        logging.info(f"Creating new bundle at {path}")

        # create the directory
        os.mkdir(path)

        # make the predicate/ and move/ directories
        for dir in [Bundle.PREDS_DIR, Bundle.MOVES_DIR]:
            os.mkdir(os.path.join(path, dir))

        # dump a bundle stub
        with open(os.path.join(path, Bundle.BUNDLE_DEFINITION_FILE), 'w') as f:
            yaml.dump({ 'format': 1 }, f)

        # and return it after loading again.  This is technically a
        # round-trip serialization/deserialization, but I'm not too
        # worried about that at the moment.
        return Bundle.load(path)

    @staticmethod
    def load(path: str) -> 'Bundle':
        """Load a bundle from disk."""
        new_bundle = Bundle()
        new_bundle.set_path(path)
        assert(isinstance(new_bundle._bundle_file, str))
        with open(new_bundle._bundle_file, 'r') as f:
            simple = yaml.load(f)

        # load the mappings from disk into this dictionary
        if simple:
            new_bundle.update(simple)

        return new_bundle

    @staticmethod
    def yaml_represent(dumper: yaml.Dumper, data: 'Bundle'):
        """PyYAML representer for a Bundle object."""
        # Make sure we'll save things in the right order, etc.
        data.normalize()
        return _yaml_represent_OrderedDict(dumper, data)

    def save(self) -> 'Bundle':
        """Save the bundle to disk."""
        if not self._bundle_file:
            raise Exception()
        with open(self._bundle_file, 'w') as f:
            yaml.dump(self, f, **Bundle.YAML_DUMP_ARGS)
        return self

    def dump(self) -> str:
        """Dump this bundle to YAML as a string."""
        # type is ignored because yaml.dump is malformed when we want to dump to string
        return yaml.dump(self, None, **Bundle.YAML_DUMP_ARGS) # type: ignore

    def _add_component(self, kind: str, component) -> 'Bundle':
        """Add a kind (predicate, move) of component."""
        assert('filename' in component)
        if kind not in self: self[kind] = list()
        for i in range(len(self[kind])):
            if component['filename'] == self[kind][i]['filename']:
                self[kind][i].update(component)
                return self
        self[kind].append(component)
        return self

    def add_predicate(self, **component) -> 'Bundle':
        """Add a predicate to the bundle."""
        return self._add_component('predicates', component)

    def add_move(self, **component) -> 'Bundle':
        """Add a move to the bundle."""
        return self._add_component('moves', component)

    def add_algorithm(self, name) -> 'Bundle':
        """Create a new algorithm in this bundle."""
        if self._find_algorithm(name):
            raise Exception()
        if 'algorithms' not in self: self['algorithms'] = list()
        self['algorithms'].append({"name": name})
        return self

    def add_rule_to_algorithm(self, algorithm_name, predicate_file, move_file) -> 'Bundle':
        """Construct and add a rule to an algorithm in this bundle."""
        pred = self._find_component('predicates', { "filename": predicate_file })
        move = self._find_component('moves', { "filename": move_file })
        alg = self._find_algorithm(algorithm_name)
        if pred is None or move is None or alg is None:
            raise Exception()
        # todo: avoid adding duplicate rules
        if 'rules' not in alg: alg['rules'] = list()
        alg['rules'].append(OrderedDict([
            ('predicate', pred),
            ('move', move)
        ]))
        return self

    def load_algorithm(self, algorithm_name: str) -> core.Algorithm:
        """Load a 'real' algorithm from this bundle."""
        alg = self._find_algorithm(algorithm_name)
        if alg is None:
            raise Exception()
        rules = list()
        if 'rules' in alg:
            for rule in alg['rules']:
                for d in [rule['predicate'], rule['move']]:
                    d['filename'] = self._canonicalize_path(d['filename'])
                pred = core.Predicate(**rule['predicate'])
                move = core.Move(**rule['move'])
                rules.append(core.Rule(pred, move))
        return core.Algorithm(rules)

    def normalize(self) -> 'Bundle':
        # if we don't have an 'algorithms' key,
        # then there's really nothing to do.
        if 'algorithms' not in self: return self

        # make sure all predicates/moves in rules are
        # first declared in 'predicates' and 'moves'.
        for algorithm in self['algorithms']:
            if 'rules' not in algorithm: continue
            for rule in algorithm['rules']:
                for key in [('predicate', 'predicates'), ('move', 'moves')]:
                    component = self._find_component(key[1], rule[key[0]])
                    if component:
                        # if we found a matching component,
                        # ensure it's the exact same reference
                        rule[key[0]] = component
                    else:
                        self._add_component(key[1], rule[key[0]])

        # move 'algorithms' to the bottom so it uses references (just
        # looks cleaner; has no function impact)
        self.move_to_end('algorithms')
        return self

    def _find_component(self, key: str, component: dict) -> Optional[dict]:
        """Find a component by a given filename."""
        if key not in self: return None
        for other in self[key]:
            if other['filename'] == component['filename']:
                return other
        return None

    def _find_algorithm(self, name: str) -> Optional[dict]:
        """Find an algorithm by a given name."""
        if 'algorithms' not in self: return None
        for alg in self['algorithms']:
            if alg['name'] == name:
                return alg
        return None

    def _canonicalize_path(self, path: str) -> str:
        """Canonicalize the given path relative to this bundle."""
        if not self._path:
            raise Exception()
        return os.path.join(self._path, path)

yaml.add_representer(Bundle, Bundle.yaml_represent)
