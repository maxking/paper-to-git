import os
from contextlib import suppress
from string import Template


__all__ = [
    'expand',
    'makedirs',
]


def expand(template, extras, template_class=Template):
    "Expand the given template using the extras dictionary."
    substitutions = dict(extras)
    return template_class(template).safe_substitute(substitutions)


def makedirs(path, mode=0o2775):
    """Create a directory hierarchy, ensuring permissions"""
    with suppress(FileExistsError):
        os.makedirs(path, mode)
