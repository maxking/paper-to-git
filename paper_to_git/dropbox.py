import dropbox

from paper_to_git.config import config


class Dropbox:
    """
    The base dropbox class to access.
    """
    def __init__(self, token):
        self.token = token
        self.dbx = None

    def initialize(self):
        assert config.initialized
        self.dbx = dropbox.Dropbox(self.token)


def initialize():
    dbox = Dropbox(config.dropbox.api_token)
    dbox.initialize()
    config.dbox = dbox
