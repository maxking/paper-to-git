from paper_to_git.models import PaperDoc, PaperFolder
from peewee import SqliteDatabase, OperationalError


__all__ = [
    'BaseDatabase',
    ]


class BaseDatabase:
    """The base database class to be used with Peewee.
    """
    def __init__(self, url):
        self.url = url
        self.db = None

    def initialize(self):
        self.db = SqliteDatabase(self.url)
        self._post_initialization()
        return self.db

    def _post_initialization(self):
        self.db.connect()
        try:
            self.db.create_tables([PaperDoc, PaperFolder])
        except OperationalError:
            # The database already exists.
            pass
