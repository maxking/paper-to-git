from peewee import SqliteDatabase, OperationalError


__all__ = [
    'BaseDatabase',
    ]


class BaseDatabase:
    """The base database class to be used with Peewee.
    """
    def __init__(self, url=None):
        self.url = url
        self.db = SqliteDatabase(None)

    def initialize(self, url=None):
        if url is not None:
            self.url = url
        else:
            raise ValueError
        self.db.init(url)
        self._post_initialization()
        return self.db

    def _post_initialization(self):
        from paper_to_git.models import PaperDoc, PaperFolder, Sync
        self.db.connect()
        try:
            self.db.create_tables([PaperDoc, PaperFolder, Sync])
        except OperationalError:
            # The database already exists.
            pass
