from peewee import SqliteDatabase, OperationalError

__all__ = [
    'BaseDatabase',
]


class BaseDatabase:
    """The base database class to be used with Peewee.
    """

    def __init__(self):
        self.path = None
        self.db = SqliteDatabase(None)

    def initialize(self, path):
        self.path = path
        self.db.init(path)
        self._post_initialization()

    def _post_initialization(self):
        from papergit.models import PaperDoc, PaperFolder, Sync
        try:
            self.db.create_tables([PaperDoc, PaperFolder, Sync])
        except OperationalError as e:
            if "already exists" in str(e):
                return
            raise
