__all__ = [
    'NoDestinationError',
    'DocDoesNotExist'
    ]


class NoDestinationError(BaseException):
    """There is no destination Git Repo configured for this Document"""


class DocDoesNotExist(BaseException):
    """The PaperDoc being requested does not exist"""
