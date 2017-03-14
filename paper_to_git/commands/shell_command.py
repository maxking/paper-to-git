import sys

from functools import partial
from paper_to_git.commands.base import BaseCommand
from paper_to_git.config import config

__all__ = [
    'ShellCommand'
]


def _start_ipython1(overrides, banner, *, debug=False):
    try:
        from IPython.frontend.terminal.embed import InteractiveShellEmbed
    except ImportError:
        if debug:
            print_exc()
        return None
    return InteractiveShellEmbed.instance(banner1=banner, user_ns=overrides)


def _start_ipython4(overrides, banner, *, debug=False):
    try:
        from IPython.terminal.embed import InteractiveShellEmbed
        shell = InteractiveShellEmbed.instance()
    except ImportError:
        if debug:
            print_exc()
        return None
    return partial(shell.mainloop, display_banner=banner, local_ns=overrides)


class ShellCommand(BaseCommand):
    """Start an interactive paper git shell."""

    name = 'shell'

    def add(self, parser, command_parser):
        self.parser = parser

    def _start_ipython(self, overrides, banner, debug):
        shell = None
        banner = config.shell.banner
        for starter in (_start_ipython4, _start_ipython1):
            shell = starter(overrides=overrides, banner=banner, debug=debug)
            if shell is not None:
                shell()
                break
        else:
            print(_('ipython is not available, set use_ipython to no'))

    def _start_python(self, overrides, banner):
        with ExitStack() as resources:
            interact(upframe=False, banner=banner, overrides=overrides)

    def process(self, args):
        banner = config.shell.banner

        overrides = dict()

        try:
            use_ipython = bool(config.shell.use_ipython)
        except ValueError:
            use_ipython = False
        if use_ipython:
            self._start_ipython(overrides=overrides, banner=banner, debug=True)
        else:
            self._start_python(overrirdes=overrides, banner=banner)
