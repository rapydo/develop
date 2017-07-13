
from develop.mytasks.package import show_release_output
from utilities.logs import get_logger
log = get_logger(__name__)


def test_release():
    """
    Avoid mocking context and get smart:
    http://j.mp/2ucsBcC
    """
    # what the runner should output
    release_output = 'hello world'
    # verify on this
    assert 'hello' in show_release_output(release_output)
