__all__ = [
    'mock_os_exists',
]


def mock_os_exists(path, original_func, value=True):
    def do_mock(input_arg):
        if input_arg == path:
            return value
        return original_func(input_arg)
    return do_mock
