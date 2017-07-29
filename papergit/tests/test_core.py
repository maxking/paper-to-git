import os
from unittest.mock import patch

from papergit.core import search_for_configuration_file
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
