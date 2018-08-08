import ssa

import argparse
import logging
from collections import OrderedDict

# todo: what to do if bundle.ssax does not exist?  a new verb, albiet backwards, called 'create'?

# ssa path/to/bundle.ssax new move relative/path/to/move.py [--copy | --hard-link | --soft-link]
# ssa path/to/bundle.ssax new algorithm 'Independent Set'
# ssa path/to/bundle.ssax add algorithm 'Independent Set' predicate.py move.py [--options]
# ssa path/to/bundle.ssax run 'Independent Set' path/to/graph.gml [--iterations=1000|n|inf]
# ssa path/to/bundle.ssax delete algorithm 'Independent Set'
# ssa path/to/bundle.ssax list predicates|moves|algorithms

def populate_parser(parser: argparse.ArgumentParser, options: dict) -> argparse.ArgumentParser:
    """Populate an ArgumentParser according to a recursive data structure.

    Special fields are prefixed with '$' (since this is a relatively
    unreasonable character to use in an expanded shell command).

    $handler: a function to handle this parser.  The ultimate value of
    this function is determined at argument-parsing-time and can be
    called with `args.run_handler(...)`.  A bit of magic can be
    achieved with the expression `args.run_handler(**vars(args))`,
    defining each of your handlers as

        def my_handler(positional_arg, positional_arg2, optional_arg=3, **kwargs)

    if you have `positional_arg`, etc. as the names of your arguments
    in the options dictionary.

    $positional: an ordered dictionary of arguments.  Right now, they
    should map to None -- in the future, argument configuration can be
    added here.

    $subparsers: declare a set of subparsers to dispatch to different
    argument parsers.  Each entry in this dictionary is a new parser
    options dictionary (i.e., this is the recursive bit).  The
    specific subparser used can be stored in a property determined by
    $destination.

    """
    if "$handler" in options:
        parser.set_defaults(run_handler=options["$handler"])
    if "$positional" in options:
        # parse out positional arguments and their configurations
        for argument, argument_config in options["$positional"].items():
            if argument_config: parser.add_argument(argument, **argument_config)
            else: parser.add_argument(argument)
    if "$options" in options:
        for argument, argument_config in options["$options"].items():
            if argument_config: parser.add_argument(argument, **argument_config)
            else: parser.add_argument(argument, default="")
    if "$subparsers" in options:
        # create a subparser-created
        subparser_creator = parser.add_subparsers(dest=options["$subparsers"]["$destination"])
        # for every subparser keyword,
        for sub, suboptions in options["$subparsers"].items():
            if sub.startswith("$"): continue # ignore $destination
            # create a subparser from the root
            # and recurse on that subparser's options
            populate_parser(subparser_creator.add_parser(sub), suboptions)
    return parser

def _load_bundle(bundle_path):
    """Convenience function to create/load a bundle."""
    if ssa.Bundle.exists(bundle_path):
        return ssa.Bundle.load(bundle_path)
    else:
        return ssa.Bundle.create(bundle_path)

def new_algorithm(bundle, name, **kwargs):
    """Add a new algorithm called `name` to `bundle`."""
    logging.info(f"New '{bundle}' algorithm name: {name}")
    _load_bundle(bundle).add_algorithm(name).save()

def _new_component(bundle_path, component_dir, file, new_name, method, **kwargs):
    """Copy a bundle component (predicate/move) to the bundle.

      - bundle_path :: this bundle (*.ssax)
      - component_dir :: the target component directory
      - file :: the file descriptor to read for the code
      - method :: what method on Bundle to use to add the component (e.g., Bundle.add_move)

    """
    import sys, os
    bundle = _load_bundle(bundle_path)

    if file is sys.stdin:
        lines = sys.stdin.readlines()
    else:
        with open(file, 'r') as f:
            lines = f.readlines()

    newpath = os.path.join(bundle_path, component_dir, new_name)

    # ensure parent directories exist
    os.makedirs(os.path.dirname(os.path.realpath(newpath)), exist_ok=True)

    with open(newpath, 'w') as f:
        f.writelines(lines)

    method(bundle, filename=os.path.relpath(newpath, bundle._path))
    bundle.save()

def new_predicate(bundle, name, **kwargs):
    """Add the predicate at the given path to the bundle."""
    logging.info(f"In bundle '{bundle}', saving predicate code from standard input to {name} (relative to the bundle).")
    import sys
    _new_component(bundle, 'predicate', sys.stdin, name, ssa.Bundle.add_predicate, **kwargs)

def new_move(bundle, name, **kwargs):
    """Add the move at the given path to the bundle."""
    logging.info(f"In bundle '{bundle}', saving move code from standard input to {name} (relative to the bundle).")
    import sys
    _new_component(bundle, 'move', sys.stdin, name, ssa.Bundle.add_move, **kwargs)

def add_rule_to(bundle, algorithm_name, predicate, move, **kwargs):
    """Add a rule to an algorithm."""
    logging.info(f"In bundle '{bundle}', adding a new rule ({predicate} => {move}) to {algorithm_name}.")
    import os
    _load_bundle(bundle).add_rule_to_algorithm(algorithm_name, os.path.join('predicate', predicate), os.path.join('move', move)).save()

def run_algorithm(bundle, algorithm_name, graph_generator_spec: str, iterations, num_graphs, **kwargs):
    """Run an algorithm from a bundle."""
    import ssa.trial
    logging.info(f"Algorithm: {algorithm_name} ({bundle})")
    logging.info(f"Generator: {graph_generator_spec}")
    logging.info(f"Iterations: {iterations}")
    logging.info(f"Graphs: {num_graphs}")

    # the spec tells us how to generate random graphs
    graph_gen_spec, *property_specs = graph_generator_spec.split(':')
    graph_gen_descriptor, *graph_gen_args = graph_gen_spec.split(',')
    # generator,arg,...:prop=generator,arg,...:...

    # try to get the right graph-generator-generator using a standard prefix
    graph_gen_parser = ssa.trial.get_graph_generator_parser(graph_gen_descriptor)
    if graph_gen_parser is None:
        raise Exception(f"unknown graph type '{graph_gen_descriptor}'")

    # resolve the graph-generator-generator to a graph-generator
    # by calling it with the arguments we were given (unpacked)
    graphgen = graph_gen_parser(*graph_gen_args)

    # build up the properties dictionary for apply_properties
    properties = dict()
    props = [p.split("=", 1) for p in property_specs]
    for prop, genspec in props:
        gen, *genargs = genspec.split(',')
        # note the solution above has no understanding of 'escaping' commas
        resolved = ssa.trial.get_value_generator(gen)
        if not resolved:
            raise Exception("unknown property randomizer")
        properties[prop] = resolved(*genargs)

    # convert our command-line arguments to the names used by ssa.trial.run
    kwargs_to_run_args = {
        "timeout": "timeout_seconds",
        "workers": "workers",
    }
    runargs = {kwargs_to_run_args[arg]: kwargs[arg] \
               for arg in kwargs.keys() if arg in kwargs_to_run_args}

    # load and run the algorithm
    algorithm = ssa.Bundle.load(bundle).load_algorithm(algorithm_name)
    results = ssa.trial.run(algorithm, lambda: ssa.trial.apply_properties(graphgen(), properties),\
                            iterations, num_graphs, **runargs)

    # report failures
    if results[False]:
        for timeline in results[False]:
            print("---")
            timeline.report()
        print(f"{len(results[False])} graph(s) above remain unstable.")
    else:
        print("All graphs converged.")

# Now that all our handler functions have been defined, we can define
# the CLI as an 'options' object for populate_parser.
CLIParser = populate_parser(argparse.ArgumentParser(), {
    "$positional": { "bundle": None },
    "$subparsers": {
        "$destination": "command",
        "new": {
            "$subparsers": {
                "$destination": "entity",
                "algorithm": {
                    "$handler": new_algorithm,
                    "$positional": OrderedDict([ ("name", None) ]),
                },
                "predicate": {
                    "$handler": new_predicate,
                    "$positional": OrderedDict([ ("name", None) ]),
                },
                "move": {
                    "$handler": new_move,
                    "$positional": OrderedDict([ ("name", None) ]),
                },
            },
        },
        "add-rule-to": {
            "$handler": add_rule_to,
            "$positional": OrderedDict([
                ("algorithm_name", None),
                ("predicate", None),
                ("move", None),
            ]),
        },
        "run": {
            "$handler": run_algorithm,
            "$positional": OrderedDict([
                ("algorithm_name", None),
                ("graph_generator_spec", None),
                ("num_graphs", { 'type': int }),
                ("iterations", { 'type': int }),
            ]),
            "$options": {
               "--timeout": { 'type': int },
               "--workers": { 'type': int },
                # todo:
                # --graph-file=graph.gml --format=gml
            },
        }
        # todo: "delete", "list"
    },
})

def run():
    """Parse and handle command line arguments."""
    import os
    if "LOG_LEVEL" in os.environ:
        logging.basicConfig(level=getattr(logging, os.environ["LOG_LEVEL"]))
    args = CLIParser.parse_args()
    args.run_handler(**vars(args))
