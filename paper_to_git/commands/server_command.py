"""
Run a flask serve as the GUI for paper-to-git.
"""

from paper_to_git.commands.base import BaseCommand
from paper_to_git.server import app

__all__ = [
    'ServeCommand'
    ]

class ServeCommand(BaseCommand):
    """Run serve command to run flask server.
    """

    name = 'serve'

    def add(self, parser, command_parser):
        self.parser = parser

    def process(self, args):
        app.run(host='127.0.0.1')
