"""
"""

import os
import paper_to_git.config.config
import paper_to_git.database

__all__ = [
    'initialize',
]


def search_for_configuration_file():
    """Search the file system for a configuration file to use."""
    # ./paper_git.cfg
    config_path = os.path.abspath('paper_git.cfg')
    if os.path.exists(config_path):
        return config_path
    # ./var/etc/paper_git.cfg
    config_path = os.path.abspath(
        os.path.join('var', 'etc', 'paper_git.cfg'))
    if os.path.exists(config_path):
        return config_path
    # ~/.paper_git.cfg
    config_path = os.path.join(os.getenv('HOME', '~'), '.paper_git.cfg')
    if os.path.exists(config_path):
        return config_path
    # None of the above configuration files exists.
    return None


def initialize(config_path=None, testing=False):
    # Initialize the system. The different steps that are initialized are:
    # - configuration
    # - database

    # Initialize the configuration first.
    if config_path is None:
        config_path = search_for_configuration_file()
        paper_to_git.config.config.load(config_path)
    # Next, initialize the database.
    config = paper_to_git.config.config
    config.db = paper_to_git.database.initialize()
