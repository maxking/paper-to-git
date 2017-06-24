"""
List the Documents and Folders
"""

from paper_to_git.commands.base import BaseCommand
from paper_to_git.models import PaperDoc, PaperFolder

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

    def process(self, args):
        if args.docs:
            for doc in PaperDoc.select():
                print(doc)

        if args.folders:
            for folder in PaperFolder.select():
                print(folder)
                for doc in folder.docs:
                    print('|----{}'.format(doc))

        if not (args.docs or args.folders):
            print("Please provide atleast one of the --docs or --folders flags")
