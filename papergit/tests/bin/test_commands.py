"""Tests for the main paper-git command line application."""

import pytest
from io import StringIO
from unittest.mock import patch

from papergit.bin.paper_git import main


class TestPaperGitCommand(object):
    """Tests for the main paper-git command."""

    def test_basic(self):
        # Test that the command runs without any errors.
        testargs = ['paper-git']
        output = StringIO()
        with patch('sys.argv', testargs), patch('sys.stdout', output):
            with pytest.raises(SystemExit):
                main()
        assert 'usage' in output.getvalue()
