"""
Publish a document.
"""

from paper_to_git.commands.base import BaseCommand
from paper_to_git.models import PaperDoc
from paper_to_git.errors import NoDestinationError

__all__ = [
    'PublishCommand',
    ]


class PublishCommand(BaseCommand):
    """Sync paper folder to git repos.
    """

    name = 'publish'

    def add(self, parser, command_parser):
        self.parser = parser
        command_parser.add_argument('id',
                                    help="The Paper Document to publish.")

    def process(self, args):
        try:
            doc = PaperDoc.get(PaperDoc.id == args.id)
        except PaperDoc.DoesNotExist:
            print("Invalid Doc, please check again!")
            return

        try:
            doc.publish()
        except NoDestinationError:
            print("This Document hasn't been setup with a git repo...")
            print("Please first add to a repo.")
            return
