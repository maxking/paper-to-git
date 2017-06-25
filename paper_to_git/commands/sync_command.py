"""
Run all the Syncs in the database.
"""

from paper_to_git.commands.base import BaseCommand
from paper_to_git.models import Sync

__all__ = [
    'SyncCommand',
    ]


class SyncCommand(BaseCommand):
    """Sync paper folder to git repos.
    """

    name = 'sync'

    def add(self, parser, command_parser):
        self.parser = parser


    def process(self, args):
        for sc in Sync.select():
            sc.sync()
