"""
"""

from papergit.commands.base import BaseCommand
from papergit.models import PaperDoc


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
            help="""Only update the existing docs, don't pull any new ones.""") # noqa
        command_parser.add_argument('id', nargs="*",
                                    help="Only update this PaperDoc")

    def process(self, args):
        if args.only_existing:
            for doc in PaperDoc.select():
                doc.get_changes()
            return

        if len(args.id):
            for doc_id in args.id:
                try:
                    doc = PaperDoc.get(PaperDoc.id == doc_id)
                    print('Updating {}'.format(doc))
                    doc.get_changes()
                except PaperDoc.DoesNotExist:
                    print('Doc with id {} does not exist...'.format(doc_id))
            return

        print("Pulling the list of paper docs...")
        PaperDoc.sync_docs()
