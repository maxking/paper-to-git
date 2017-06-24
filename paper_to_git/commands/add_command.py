"""
Add a new sync object to sync between a git repo and Dropbox Paper.
"""
import os

from paper_to_git.commands.base import BaseCommand
from paper_to_git.models import Sync, PaperFolder


__all__ = [
    'AddCommand',
    ]


class AddCommand(BaseCommand):
    """Add a new sync object between paper and git.
    """

    name = 'add'

    def add(self, parser, command_parser):
        self.parser = parser
        command_parser.add_argument('--repo',
                                    help='The path to the git repo.')
        command_parser.add_argument('--path',
                                    help='The path inside the repo')
        command_parser.add_argument('--folder',
                                    help='The folder name in the Paper')

    def process(self, args):
        repo = os.path.abspath(args.repo)
        path = args.path
        for folder in PaperFolder.select():
            if folder.name.lower() == args.folder.lower():
                paper_folder = folder
        Sync.create(repo=repo, path_in_repo=path, folder=paper_folder)
