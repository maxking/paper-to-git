"""

"""


import os
import re
import dropbox
import contextlib

from dropbox.paper import ExportFormat


DATA_DIR = '/home/maxking/Documents/dropbox-sdk-python/data/'

def get_dropbox_handle(access_token):
    """Given an access_token returns an instance of dropbox.Dropbox
 
    Args:
        access_token(str): the access token for your dropbox app.

    Returns:
        An instance of dropbox.Dropbox
    """
    return dropbox.Dropbox(access_token)


def get_doc_ids(dbx):
    """Fetches all the doc ids from the given dropbox handler.
 
    Args:
        dbx(dropbox.Dropbox): an instance of initialized dropbox handler

    Returns:
        An array of all the doc ids.

    Raises:
    """
    docs = dbx.paper_docs_list()
    for doc in docs.doc_ids:
        yield doc


def get_doc_details(dbx, doc_id):
    """Returns the doc's title and revision number.

    Args:
        dbx(dropbox.Dropbox):  an instance of initialized dropbox handler
        doc_id(str): document id of the document to retrieve title for.
 
    Returns:
        - The title (string) of the document.
        - The current revision(int) number of the document.
        - The list of folders that this document belongs to.

    Raises:
        ValueError
    """
    result, response = dbx.paper_docs_download(doc_id, ExportFormat.markdown)
    if response.status_code == 200:
        response.close()
    else:
        raise dropbox.exceptions.APIError

    folder_info = dbx.paper_docs_get_folder_info(doc_id)
    return (result.title, result.revision, folder_info.folders)


def sync(dbx, ids=None, export_format=ExportFormat.markdown):
    """Sync the documents in the data directory with proper directory structure as
    found in Dropbox Paper. Sync only the given ids if Arg(id) is not None.

    It raises ValueError if one or more of the IDs are not found.

    Args:
        dbx(dropbox.Dropbox):  an instance of initialized dropbox handler
        ids([str]): A list of document ids(strings).

    Returns:
        None

    Raises:
        ValueError
    """
    # TODO: validate the input to be a list of strings.

    for doc_id in get_doc_ids(dbx):
        title, revision, folders = get_doc_details(dbx, doc_id)

        # TODO: Handle multiple folders. For now, only folder is used, the first
        # one. It may lead to some random behaviour if the return output of
        # folders is not sorted and is random everytime. Make sure to check back
        # on this ASAP.

        doc_path = get_path(title, folders)
        dbx.paper_docs_download_to_file(doc_path, doc_id, export_format)


def get_path(title, folders):
    """Return the absolute path to the document in the DATA_DIR. Use the
    first folder if the document belongs to multiple folders.

    This also creates the folder if it does not exist.

    Args:
        title(str): This is the title of the document.
        folders([str]): These are the folders that this document belongs to.

    Returns:
        Full path to the document.
    """
    if folders is None:
        folder = ''
    else:
        folder = folders[0].name

    folder_path = os.path.join(DATA_DIR, folder)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    return os.path.join(folder_path, title_to_name(title))


def title_to_name(title, file_extension='.md'):
    """Given the title of a document returns the filename that should be used
    to sync the document.

    Args:
        title(str): The title of the document.
        file_extension(str): The extension of the filename.

    Returns:
        the file name of the document with with the given extension.
    """
    regex = re.compile('[\s+,.]')
    return regex.sub('-', title.strip()) + file_extension

if __name__ == '__main__':
    main()
