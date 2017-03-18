"""
"""
import dropbox.exceptions

from dropbox.paper import ExportFormat
from paper_to_git.utilities.dropbox import dropbox_api
from paper_to_git.config import config
from peewee import (Model, CharField, ForeignKeyField, IntegerField)


__all__ = [
    'PaperDoc',
    'PaperFolder',
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

    def __repr__(self):
        return "Folder {}".format(self.name)


class PaperDoc(BasePaperModel):
    """Representation of a Dropbox Paper document."""
    title = CharField()
    paper_id = CharField()
    version = IntegerField(default=0)
    folder = ForeignKeyField(PaperFolder, null=True)

    def __init__(self, paper_id, *args, **kwargs):
        super().__init__(paper_id, *args, **kwargs)
        self.paper_id = paper_id
        self._post_create()

    def __repr__(self):
        return "Document {} at version {}".format(self.title, self.version)

    def _post_create(self):
        title, rev = self._get_doc_details()
        self.title = title
        self.version = rev
        # self.save()
        # TODO: Set paper folder also.

    def get_by_paper_id(self, paper_id):
        return PaperDoc.get(PaperDoc.paper_id == paper_id)

    def update(self):
        """
        Pull a list of all the docs from dropbox
        """
        pass

    @classmethod
    @dropbox_api
    def get_docs(self, dbx):
        """Fetches all the doc ids from the given dropbox handler.
        Args:
            dbx(dropbox.Dropbox): an instance of initialized dropbox handler
        Returns:
            An array of all the doc ids.
        """
        docs = dbx.paper_docs_list()
        for doc in docs.doc_ids:
            try:
                yield PaperDoc.get(PaperDoc.paper_id == doc)
            except PaperDoc.DoesNotExist:
                yield PaperDoc(doc)

    @dropbox_api
    def _get_doc_details(self, dbx):
        """Returns the doc's title and revision number.

        Args:
            dbx(dropbox.Dropbox):  an instance of initialized dropbox handler
            doc_id(str): document id of the document to retrieve title for.
        Returns:
            - The title (string) of the document.
            - The current revision(int) number of the document.
            - The list of folders that this document belongs to.
        """
        result, response = dbx.paper_docs_download(
                           self.paper_id, ExportFormat.markdown)
        if response.status_code == 200:
            response.close()
        else:
            raise dropbox.exceptions.APIError
        return (result.title, result.revision)

    # def sync(self, dbx, ids=None, export_format=ExportFormat.markdown):
    #     """Sync the documents in the data directory with proper directory structure as
    #     found in Dropbox Paper. Sync only the given ids if Arg(id) is not None.

    #     It return aises ValueError if one or more of the IDs are not found.

    #     Args:
    #         dbx(dropbox.Dropbox):  an instance of initialized dropbox handler
    #         ids([str]): A list of document ids(strings).

    #     Returns:
    #         None

    #     Raises:
    #         ValueError
    #     """
    #     # TODO: validate the input to be a list of strings.
    #     for doc_id in get_doc_ids(dbx):
    #         title, revision, folders = get_doc_details(dbx, doc_id)

    #         # TODO: Handle multiple folders. For now, only folder is used, the
    #         # first one. It may lead to some random behaviour if the return
    #         # output of folders is not sorted and is random everytime. Make
    #         # sure to check back on this ASAP.

    #         doc_path = get_path(title, folders)
    #         dbx.paper_docs_download_to_file(doc_path, doc_id, export_format)
