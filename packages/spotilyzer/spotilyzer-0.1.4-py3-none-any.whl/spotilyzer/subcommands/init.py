"""
spotilyzer init subcommand
"""

# system imports
import os
import shutil

# project imports
from .base import SubCommand
from .utils.paths import get_package_datadir, get_user_datadir, SEEDS_FILE

# constants
_DESCRIPTION = "initialize spotilyzer"
_SEEDS_FILE = 'seeds.json'


class Init(SubCommand):

    name = 'init'

    @classmethod
    def add_parser(cls, subparsers):
        subparsers.add_parser(cls.name, description=_DESCRIPTION,
                              help=_DESCRIPTION)

    def run(self):
        spotilyzer_dir = get_user_datadir()
        os.makedirs(spotilyzer_dir, exist_ok=True)
        if not os.path.exists(os.path.join(spotilyzer_dir, SEEDS_FILE)):
            seeds_file = os.path.join(get_package_datadir(), SEEDS_FILE)
            shutil.copy(seeds_file, spotilyzer_dir)
