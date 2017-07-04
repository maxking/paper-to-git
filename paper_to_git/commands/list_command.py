"""
List the Documents and Folders
"""

from paper_to_git.commands.base import BaseCommand
from paper_to_git.models import PaperDoc, PaperFolder, Sync

__all__ = [
    'ListCommand',
    ]


class ListCommand(BaseCommand):
    """List the PaperDocs and Folders
    """

    name = 'list'

    def add(self, parser, command_parser):
        self.parser = parser
        command_parser.add_argument('-d', '--docs',
            default=False, action='store_true',
            help=("""\
            List all the documents currently stored."""))
        command_parser.add_argument('-fd', '--folders',
            default=False, action='store_true',
            help=("""List all folders in Dropbox Paper"""))
        command_parser.add_argument('-sc', '--sync',
            default=False, action='store_true',
            help=("""List all the sync objects"""))

    def process(self, args):
        if args.docs:
            for doc in PaperDoc.select():
                print(doc)

        if args.folders:
            for folder in PaperFolder.select():
                print(folder)
                for doc in folder.docs:
                    print('|----{}'.format(doc))

        if args.sync:
            for sync in Sync.select():
                print(sync)

        if not (args.docs or args.folders or args.sync):
            # if no args provided, list all the documents that were recently
            # updated.
            for doc in PaperDoc.select().order_by(
                    PaperDoc.last_updated.desc()).limit(5):
                print(doc)
