# -*- coding: utf-8 -*-

from invoke import task
# from develop import execution as exe
from develop import config
from utilities.logs import get_logger

log = get_logger(__name__)


@task
def version(ctx, path=None):
    """ Check current rapydo version """

    if path is None:
        path = config.components_path(ctx)

    pass
