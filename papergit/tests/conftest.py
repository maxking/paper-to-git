import pytest

from papergit.core import initialize
from string import Template


TESTING_CONFIG = Template("""\
[main]
layout: testing

[paths.testing]
var_dir: $dir

[dropbox]
api_token: SomeRandomApiToken
""")


@pytest.fixture(scope="session")
def initialize_fixture(tmpdir_factory, request):
    print("\nInitializing tests ...\n")
    testing_dir = tmpdir_factory.mktemp('var')
    testing_config = testing_dir.join('paper-git.cfg')
    with testing_config.open(ensure=True, mode='w') as f:
        print(TESTING_CONFIG.substitute(dir=str(testing_dir)), file=f)
    initialize(testing=True, config_path=str(testing_config))

    def teardown():
        print("\nTearing down ...\n")

    request.addfinalizer(teardown)
