"""The paper_git command dispatcher"""


import argparse

from paper_to_git.core import initialize
from paper_to_git.commands.base import BaseCommand
from paper_to_git.utilities.modules import find_components


def main():
    """The `paper_git command dispatcher."""
    parser = argparse.ArgumentParser(
        description="""\
        The Paper-to-Git system
        Copyright 2017 Abhilash Raj""",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparser = parser.add_subparsers(title='Commands')
    subcommands = []
    for command_class in find_components('paper_to_git.commands', BaseCommand):
        command = command_class()
        assert issubclass(command_class, BaseCommand)
        subcommands.append(command)
    for command in subcommands:
        command_parser = subparser.add_parser(
            command.name, help=command.__doc__)
        command.add(parser, command_parser)
        command_parser.set_defaults(func=command.process)

    args = parser.parse_args()

    if len(args.__dict__) < 1:
        # No arguments or subcommands were given.
        parser.print_help()
        parser.exit()
    # Initialize the system.
    initialize()
    # Run the given command.
    args.func(args)
