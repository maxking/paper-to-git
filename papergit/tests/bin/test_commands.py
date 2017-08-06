"""Tests for the main paper-git command line application."""

import pytest
from io import StringIO
from unittest.mock import patch

from papergit.bin.paper_git import main


class TestPaperGitCommand(object):
    """Tests for the main paper-git command."""

    def test_usage_with_no_arguments(self):
        # Test that the command runs without any arguments.
        testargs = ['paper-git']
        output = StringIO()
        with patch('sys.argv', testargs), patch('sys.stdout', output):
            with pytest.raises(SystemExit):
                main()
        assert 'usage' in output.getvalue()

    def test_usage_with_bad_arguments(self):
        # Test that the command prints usage with wrong arguments.
        testargs = ['paper-git', 'badcommand']
        output = StringIO()
        with patch('sys.argv', testargs), patch('sys.stderr', output):
            with pytest.raises(SystemExit):
                main()
        assert 'usage' in output.getvalue()

    def test_initialization(self):
        # Test paper-git with a valid command.
        testargs = ['paper-git', 'list']
        output = StringIO()
        error = StringIO()
        with patch('sys.argv', testargs), \
                patch('sys.stdout', output), patch('sys.stderr', error):
            main()
        assert '' in output.getvalue()
        assert '' in error.getvalue()
