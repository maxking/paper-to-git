"""
"""
import os
import time
import dropbox.exceptions

from dropbox.paper import ExportFormat
from git import Repo, GitCommandError
from paper_to_git.utilities.dropbox import dropbox_api
from paper_to_git.utilities.modules import create_file_name
from paper_to_git.config import config
from peewee import ( Model, CharField, ForeignKeyField, IntegerField,
                     TimestampField, PrimaryKeyField)


__all__ = [
    'PaperDoc',
    'PaperFolder',
    'Sync',
    ]


class BasePaperModel(Model):
    """This is base model from Dropbox Paper. All the paper documents
    be it folder or document subclass this. It provides some very basic
    functionalities.
    """
    class Meta:
        database = config.db.db


class PaperFolder(BasePaperModel):
    """Representation of a Dropbox Paper folder"""
    name = CharField()
    folder_id = CharField()

    def __repr__(self):
        return "Folder {}".format(self.name)


class PaperDoc(BasePaperModel):
    """Representation of a Dropbox Paper document."""
    title = CharField()
    paper_id = CharField()
    version = IntegerField(default=0)
    folder = ForeignKeyField(PaperFolder, null=True, related_name='docs')
    last_updated = TimestampField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return "Document {} at version {}".format(self.title, self.version)

    @classmethod
    def get_by_paper_id(self, paper_id):
        return PaperDoc.get(PaperDoc.paper_id == paper_id)

    def get_changes(self):
        """Update this record with the latest version of the document. Also,
        download the latest version to the file.
        """
        title, rev = PaperDoc.download_doc(self.paper_id)
        if rev > self.version:
            print('Update revision for doc {0} from {1} to {2}'.format(
                  self.title, self.version, rev))
            self.version = rev
            self.last_updated = time.time()
        if self.title != title:
            self.title = title
            self.last_updated = time.time()
        self.save()
        self.update_folder_info()

    @classmethod
    def generate_file_path(self, doc_id):
        return os.path.join(config.CACHE_DIR, doc_id + '.md')

    @classmethod
    @dropbox_api
    def sync_docs(self, dbx):
        """Fetches all the doc ids from the given dropbox handler.
        Args:
            dbx(dropbox.Dropbox): an instance of initialized dropbox handler
        Returns:
            An array of all the doc ids.
        """
        docs = dbx.paper_docs_list()
        for doc_id in docs.doc_ids:
            try:
                doc = PaperDoc.get(PaperDoc.paper_id == doc_id)
                if not os.path.exists(self.generate_file_path(doc_id)):
                    self.download_doc(doc_id)
            except PaperDoc.DoesNotExist:
                title, rev = self.download_doc(doc_id)
                doc = PaperDoc.create(paper_id=doc_id, title=title, version=rev,
                                      last_updated=time.time())
                doc.update_folder_info()
            print(doc)

    @classmethod
    @dropbox_api
    def download_doc(self, dbx, doc_id):
        """Downloads the given doc_id to the local file cache.
        """
        path = self.generate_file_path(doc_id)
        result = dbx.paper_docs_download_to_file(
            path, doc_id, ExportFormat.markdown)
        return (result.title, result.revision)

    @dropbox_api
    def update_folder_info(self, dbx):
        """Fetch and update the folder information for the current PaperDoc.
        """
        folders = dbx.paper_docs_get_folder_info(self.paper_id)
        if folders.folders is None:
            return
        folder = folders.folders[0]
        f = PaperFolder.get_or_create(folder_id=folder.id, name=folder.name)[0]
        self.folder = f
        self.save()


class Sync(BasePaperModel):
    """Representation of a synchronization between a Git repo and a
    PaperFolder. Files are synchronized only after a few changes are made and
    the metadata is added.

    Files with #draft in them is not synchronized to the git repo.
    """
    # Path to the Git Repo.
    repo = CharField()
    # Path to the directories in the git repo.
    path_in_repo = CharField()
    folder = ForeignKeyField(PaperFolder)

    def __repr__(self):
        return "Git repo at {} to Folder {}".format(repo, folder.name)

    def sync(self):
        for doc in self.folder.docs:
            original_path = PaperDoc.generate_file_path(doc.paper_id)
            file_name = create_file_name(doc.title)
            final_path = os.path.join(self.repo, self.path_in_repo, file_name)
            with open(final_path, 'w') as fp:
                with open(original_path, 'r') as op:
                    print(op.read(), file=fp)
        self.commit_changes()

    def commit_changes(self):
        git_repo = Repo(self.repo)
        git_repo.git.add(A=True)
        try:
            git_repo.git.commit('-m', 'A random git message.')
        except GitCommandError:
            print('Nothing to commit')
            pass
