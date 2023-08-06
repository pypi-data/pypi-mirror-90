"""
spotilyzer driver
"""

# project imports
from .subcommands import subcommands
from .cli import SUBCOMMAND_ARG


def run(args):
    name = getattr(args, SUBCOMMAND_ARG)
    for subcommand in subcommands:
        if name == subcommand.name:
            subcommand(args).run()
            return
    raise NotImplementedError(f"subcommand {name} not implemented")
