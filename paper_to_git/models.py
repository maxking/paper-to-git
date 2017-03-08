"""
"""

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
    pass


class PaperDoc(BasePaperModel):
    title = CharField()
    paper_id = CharField()
    version = IntegerField()
    folder = ForeignKeyField(PaperFolder, related_name='docs')

    def __repr__(self):
        return "Document {} at version {}".format(self.title, self.version)


    def update(self):
        """
        Pull a list of all the docs from dropbox
        """

class PaperFolder(BasePaperModel):
    name = CharField()
    docs = ForeignKeyField(PaperDoc, related_name='folder')

    def __repr__(self):
        return "Folder {}".format(self.name)
