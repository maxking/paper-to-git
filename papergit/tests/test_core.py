import os
import peewee
import pytest

from unittest.mock import patch
from papergit.config import config
from papergit.core import (
    search_for_configuration_file, initialize_1, initialize)
from papergit.utilities.testing import mock_os_exists


class TestInitialization(object):

    # Patch the function to always return true for /etc/paper-git.cfg
    def test_search_config_file(self, tmpdir_factory, monkeypatch):
        with patch('os.path.exists',
                   mock_os_exists('/etc/paper-git.cfg', os.path.exists)):
            # Search for the configuration file.
            test_dir = tmpdir_factory.mktemp('testdir')
            # Add a config file at ./paper-git.cfg, './var/etc/paper-git.cfg
            test_config1 = test_dir.join('paper-git.cfg')
            test_config1.write('# This is a testing configuration file.')
            test_config2 = test_dir.join('var/etc/paper-git.cfg')
            with test_config2.open(ensure=True, mode='w') as fp:
                print('# This is a testing configuration file.', file=fp)

            with test_dir.as_cwd():
                assert search_for_configuration_file() == str(test_config1)
            # Remove the config file at ./paper-git.cfg
            os.remove(str(test_config1))

            # Test if the configuration is present at var/etc/paper-git.cfg
            with test_dir.as_cwd():
                assert search_for_configuration_file() == str(test_config2)
            os.remove(str(test_config2))

            assert search_for_configuration_file() == '/etc/paper-git.cfg'

        # No configuration file exists.
        with patch('os.path.exists', return_value=False):
            assert search_for_configuration_file() is None

    def test_initialize_1_with_config(self, tmpdir_factory):
        var_dir = tmpdir_factory.mktemp('temp_var')
        test_config = var_dir.join('paper-git.cfg')
        with test_config.open(ensure=True, mode='w') as fp:
            print("""
[dropbox]
api_token: thisisarandomvalueofapitoken
            """, file=fp)
        with var_dir.as_cwd():
            assert not config.initialized
            initialize_1(config_path=str(test_config))
        assert config.initialized
        assert config.dropbox.api_token == 'thisisarandomvalueofapitoken'

    def test_initialize_1_without_config(self, tmpdir_factory):
        var_dir = tmpdir_factory.mktemp('temp_var')
        test_config = var_dir.join('paper-git.cfg')
        with test_config.open(ensure=True, mode='w') as fp:
            print("""
[dropbox]
api_token: thisisadifferentapitoken
            """, file=fp)
        with var_dir.as_cwd():
            initialize_1()
        assert config.initialized
        assert config.dropbox.api_token == 'thisisadifferentapitoken'

    def test_initialize_2(self, tmpdir_factory):
        var_dir = tmpdir_factory.mktemp('temp_var')
        test_config = var_dir.join('paper-git.cfg')
        with test_config.open(ensure=True, mode='w') as fp:
            print("""
[dropbox]
api_token: thisisanotherapikey
            """, file=fp)
        assert config.dbox is None
        assert config.db.path is None
        with pytest.raises(peewee.OperationalError):
            config.db.db.connect()
        with var_dir.as_cwd():
            initialize()
        # Make sure that the database connection works.
        assert config.db.path is not None
        assert set(config.db.db.get_tables()) == set([
            'paperdoc', 'paperfolder', 'sync'])
        assert config.dbox is not None
