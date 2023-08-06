"""
spotilyzer cli utilities
"""

# system imports
import argparse


def options(name, shortname=None):
    return f'-{shortname is None and name[0] or shortname}', \
           f'--{name}'


def posint(string):
    try:
        value = int(string)
    except ValueError as e:
        raise argparse.ArgumentTypeError(e)
    if value < 1:
        raise argparse.ArgumentTypeError(f"invalid value {string}: value must "
                                         "be greater than 0")
    return value


def posfloat(string):
    try:
        value = float(string)
    except ValueError as e:
        raise argparse.ArgumentTypeError(e)
    if value < 0.0:
        raise argparse.ArgumentTypeError(f"invalid value {string}: value must "
                                         "be greater than or equal to 0.0")
    return value


def csv(string):
    return string.split(',')
