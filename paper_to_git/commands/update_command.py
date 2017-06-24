"""
"""

from paper_to_git.commands.base import BaseCommand
from paper_to_git.models import PaperDoc


__all__ = [
    'UpdateCommand',
    ]


class UpdateCommand(BaseCommand):
    """Pull the list of Paper docs and update the database."""

    name = 'update'

    def add(self, parser, command_parser):
        self.parser = parser
        command_parser.add_argument('--only-existing',
            default=False, action='store_true',
            help="""Only update the existing docs, don't pull any new ones.""")

    def process(self, args):
        if args.only_existing:
            for doc in PaperDoc.select():
                doc.get_changes()
            return
        print("Pulling the list of paper docs...")
        PaperDoc.sync_docs()
