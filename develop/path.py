# -*- coding: utf-8 -*-

from pathlib import Path
from utilities.logs import get_logger

log = get_logger(__name__)


def build(path):
    p = Path(path)
    return p


def home(relative_path=None):
    if relative_path is None:
        return Path.home()
    else:
        if relative_path.startswith('/'):
            log.exit(
                "Requested abspath '%s' in relative context" % relative_path)
        return build('~/' + relative_path).expanduser()


def current():
    return Path.cwd()
