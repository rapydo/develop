
from develop.mytasks import package, release, repo
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
    assert '<module' in str(repo)

    # FIXME: add some checks at least in init/status
    assert True
