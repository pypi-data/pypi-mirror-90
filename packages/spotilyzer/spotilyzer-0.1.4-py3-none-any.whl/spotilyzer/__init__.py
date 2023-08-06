"""
spotilyzer entry point
"""

# system imports
import sys

# project imports
from .cli import parse_cmdline
from .driver import run


def main(argv=sys.argv):
    try:
        args = parse_cmdline(argv)
        run(args)
    except SystemExit as e:
        return e
    except Exception as e:
        print(f"[error]: {e}")
        return 1
    return 0
