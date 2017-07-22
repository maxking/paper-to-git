"""
"""

from string import Template
from papergit.config import config

__all__ = [
    'generate_metadata',
    ]


METADATA_TEMPLATE = Template("""\
---
title: "$title"
date: "$date"
---

""")


def generate_metadata(doc, metadata_type=None):
    """
    Generate the appropriate metadata based on the type specified.
    """
    if metadata_type is None:
        metadata_type = config.metadata.type

    if metadata_type == "yaml":
        return generate_yaml_metadata(doc)
    raise NotImplementedError


def generate_yaml_metadata(doc):
    """
    Generate the YAML metadata to add on top of a PaperDoc when moving a
    PaperDoc to a static site generator.
    """
    return METADATA_TEMPLATE.safe_substitute(title=doc.title,
                                             date=doc.last_updated)
