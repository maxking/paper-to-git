#! /usr/bin/env python3

# Use this program to sync all the documents from your dropbox paper account.
#
# See README.md to see the usage.


import os
import sys
import dropbox
import src.paper_to_git as pg


def usage():
    print("""\
 ./paper-sync.py API_TOKEN DATA_DIR

 API_TOKEN: Your dropbox API Token.
 DATA_DIR: Full path to the directory you wan to save your documents in
    """)


def main(api_token, data_dir):
    """Use the API token to sync all the documents in dropbox paper to the given
    data directory


    Args:
        api_token(str): Dropbox api token
        data_dir(str): Full or relative path to the directory where everything
                       is to be synced.
    """
    dbx = dropbox.Dropbox(api_token)
    pg.DATA_DIR = os.path.abspath(data_dir)
    pg.sync(dbx)


if __name__ == '__main__':

    if len(sys.argv) < 3:
        usage()

    main(api_token=sys.argv[1], data_dir=sys.argv[2])
