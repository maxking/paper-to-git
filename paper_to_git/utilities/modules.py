"""
"""

import os
import sys

from contextlib import suppress
from string import Template
from pkg_resources import resource_listdir
from paper_to_git.config import config

__all__ = [
    'expand',
    'makedirs',
    'find_components',
    'dropbox_api',
    ]


def expand(template, extras, template_class=Template):
    """Expand the given template using the extras dictionary."""
    substitutions = dict(extras)
    return template_class(template).safe_substitute(substitutions)


def makedirs(path, mode=0o2775):
    """Create a directory hierarchy, ensuring permissions"""
    with suppress(FileExistsError):
        os.makedirs(path, mode)


def scan_module(module, base_class):
    """Return all the items in a module that are subclass of a given base class.
    """
    missing = object()
    for name in module.__all__:
        component = getattr(module, name, missing)
        assert component is not missing, (
            '{} has bad __all__: {}'.format(module, name))
        if issubclass(component, base_class):
            yield component


def find_components(package, base_class):
    """Find components which are subclass of a given base class.
    """
    for filename in resource_listdir(package, ''):
        basename, extension = os.path.splitext(filename)
        if extension != '.py' or basename.startswith('.'):
            continue
        module_name = "{}.{}".format(package, basename)
        __import__(module_name, fromlist='*')
        module = sys.modules[module_name]
        if not hasattr(module, '__all__'):
            continue
        yield from scan_module(module, base_class)


def dropbox_api(function):
    """
    Attach a global dropbox handler with the function.
    """
    def func_wrapper(*args, **kwargs):
        print(config)
        dbx = config.dbox.dbx
        if len(args) > 0:
            return function(args[0], dbx, *args[1:], **kws)
        else:
            return function(dbx, **kws)
    return func_wrapper


class dbconnection(object):
    """
    """
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kws):
        db = config.db
        db.connect()
        if len(args) > 0:
            self.f(args[0], db, *args[1:], **kws)
        else:
            self.f(db, **kws)
        db.close()
