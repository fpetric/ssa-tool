#!/usr/bin/env python3
import ssa
import networkx as nx

# ./ssa-tool.py run "independent set" from ind-set.ssax on test.gexf

def parse_args(argv):
    if argv[1] == 'run':
        assert (argv[1], argv[3], argv[5]) == ('run', 'from', 'on')
        
        algorithm = argv[2]
        bundle    = argv[4]
        graph     = argv[6]

        graphfmt = graph.split('.')[-1]
        if graphfmt == graph:
            raise Exception('no graph format given')
        if graphfmt not in ['gexf', 'gml', 'yaml']:
            raise Exception('unrecognized graph format')

        return {
            'command'   : 'run',
            'bundle'    : bundle,
            'algorithm' : algorithm,
            'graph'     : graph,
            'graphfmt'  : graphfmt
        }

def non_interactive(args):
    args = parse_args(args)
    if args['command'] == 'run':
        print('''Running:
  Algorithm: "{algorithm}"
       from: "{bundle}"
         on: "{graph}"
    (format: "{graphfmt}")'''.format(**args))
        b = ssa.Bundle(args['bundle'])
        # add from_name to Bundle
        a = list(filter(lambda e: e.name == args['algorithm'],
                        b.entities))[0]

        reader = {'gexf': nx.read_gexf, # require pyparsing
                  'gml': nx.read_gml,
                  'yaml': nx.read_yaml
        }[args['graphfmt']]
        G = reader(args['graph'])
        from pprint import pprint
        print('Read Graph:')
        pprint(G.nodes(data=True))
        print('History:')
        pprint(a.run(G, 10))
        print('Stable Graph:')
        pprint(G.nodes(data=True))

print('Welcome to SSA-Tool, version 1.')
import sys
if '--non-interactive' in sys.argv:
    non_interactive(sys.argv)
else:
    import gui
    gui.root.mainloop()
