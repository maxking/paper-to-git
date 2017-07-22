"""
Add a new sync object to sync between a git repo and Dropbox Paper.
"""
import os

from papergit.commands.base import BaseCommand
from papergit.models import Sync, PaperFolder


__all__ = [
    'AddCommand',
    ]


class AddCommand(BaseCommand):
    """Add a new sync object between paper and git.
    """

    name = 'add'

    def add(self, parser, command_parser):
        self.parser = parser
        command_parser.add_argument('--repo', required=True,
                                    help='The path to the git repo.')
        command_parser.add_argument('--path', required=True,
                                    help='The path inside the repo')
        command_parser.add_argument('--folder', required=True,
                                    help='The folder name in the Paper')

    def process(self, args):
        repo = os.path.abspath(args.repo)
        path = args.path
        paper_folder = None
        for folder in PaperFolder.select():
            if folder.name.lower() == args.folder.lower():
                paper_folder = folder
        if paper_folder is None:
            print("No such PaperFolder exists!")
            return
        if not os.path.exists(os.path.join(repo, path)):
            print("The destination path to git repo doesn't exist...")
            return
        Sync.create(repo=repo, path_in_repo=path, folder=paper_folder)
