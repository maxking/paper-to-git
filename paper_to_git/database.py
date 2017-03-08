from paper_to_git.config import config
from paper_to_git.utilities import expand

from peewee import SqliteDatabase

__all__ = [
    'initialize'
    ]


class BaseDatabase:
    """The base database class to be used with Peewee.
    """
    def __init__(self):
        self.url = None
        self.db = None

    def initialize(self):
        assert config.initialized
        url = expand(config.database.url, config.paths)
        self.url = url
        self.db = SqliteDatabase(self.url)
        return self.db


def initialize():
    """
    Global database initialization.
    """
    db = BaseDatabase()
    return db.initialize()
