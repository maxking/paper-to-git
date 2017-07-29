import os

__all__ = [
    'mock_os_exists',
]


def mock_os_exists(path):
    def do_mock(input_arg):
        if input_arg == path:
            return True
        return os.path.exists(input_arg)
    return do_mock
