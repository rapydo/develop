# -*- coding: utf-8 -*-

from invoke import task
# from develop import execution as exe
from develop import config
from utilities import helpers
# from develop import cycles
from utilities.logs import get_logger

log = get_logger(__name__)


@task
def version(ctx, path=None):
    """ Check current rapydo version """

    if path is None:
        path = config.components_path(ctx)

    pass


@task
def init(ctx, version=None):
    """ Initialize the RAPyDo framework on your machine """

    base_path = config.main_path(ctx)
    log.debug('Base path: %s', base_path)
    components_path = config.components_path(ctx)
    projects_path = config.projects_path(ctx)

    paths = [base_path, components_path, projects_path]

    for element in paths:
        if not element.exists():
            helpers.ask_yes_or_no(
                'Path %s not existing (or no permissions).\n' % element +
                'Do you want me to create it?',
                error='Unable to continue.'
            )
            print("TEST", element)
