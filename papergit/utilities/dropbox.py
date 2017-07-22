__all__ = [
    'dropbox_api'
    ]


def dropbox_api(function):
    """
    Attach a global dropbox handler with the function.
    """
    def func_wrapper(*args, **kws):
        # Avoid circular imports.
        from papergit.config import config
        dbx = config.dbox.dbx
        if len(args) > 0:
            return function(args[0], dbx, *args[1:], **kws)
        else:
            return function(dbx, **kws)
    return func_wrapper
