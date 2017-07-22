import dropbox

from dropbox import DropboxOAuth2FlowNoRedirect
from papergit.config import config


class Dropbox:
    """
    The base dropbox class to access.
    """
    def __init__(self):
        self.dbx = None

    def initialize(self):
        assert config.initialized
        self.dbx = dropbox.Dropbox(self.get_auth_token())

    def get_old_auth_token(self):
        # Check if the OAuth Flow has been performed before and thus doesn't
        # need to be done again. If yes, return the auth_token
        token = getattr(config.dropbox, 'api_token')
        return None if token == '' else token

    def get_auth_token(self):
        old_token = self.get_old_auth_token()
        if old_token is None:
            # This means that we don't have the authentication token, so run the
            # entire workflow again to get the auth token.
            return self.get_new_auth_token()
        # If not none, just return the old Auth Token
        return old_token

    def get_new_auth_token(self):
        # Run the dropbox OAuth Flow to get the user's OAuth Token.
        auth_flow = DropboxOAuth2FlowNoRedirect(config.dropbox.app_key,
                                                config.dropbox.app_secret)
        authorize_url = auth_flow.start()
        print("1. Go to: " + authorize_url)
        print("2. Click \"Allow\" (you might have to log in first).")
        print("3. Copy the authorization code.")
        auth_code = input("Enter the authorization code here: ").strip()

        try:
            oauth_result = auth_flow.finish(auth_code)
        except Exception as e:
            print('Error: %s' % (e,))
            return

        config.write_to_user_config('dropbox', 'api_token',
                                    oauth_result.access_token)
        return oauth_result.access_token


def initialize():
    dbox = Dropbox()
    dbox.initialize()
    config.dbox = dbox
