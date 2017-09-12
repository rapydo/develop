
from develop.mytasks import package, release
from utilities.logs import get_logger
log = get_logger(__name__)


def test_release():
    """
    Avoid mocking context and get smart:
    http://j.mp/2ucsBcC
    """

    # check modules
    assert '<module' in str(release)
    assert '<module' in str(package)

    # what the runner should output
    release_output = 'hello world'
    # verify on this
    assert 'hello' in package.show_release_output(release_output)
