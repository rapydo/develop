# -*- coding: utf-8 -*-

from invoke import task
# from develop import execution as exe
from develop import config
from utilities import helpers
from develop import cycles
from utilities.logs import get_logger

log = get_logger(__name__)


@task
def version(ctx, path=None):
    """ Check current rapydo version """

    if path is None:
        path = config.components_path(ctx)

    pass


def initialize_tool(name, path, version):

    if not path.exists():
        helpers.ask_yes_or_no(
            'Component: %s' % name +
            '\nPath %s not existing (or no permissions).\n' % path +
            'Do you want me to create it?',
            error='Unable to continue.'
        )
        print("TEST", path)
        raise NotImplementedError("to do!")
        exit(1)
    else:
        log.checked("Found")


def initialize_project(name, path, version):
    print("TEST", name, path, version)


def initialize_cli(name, path, version):
    pass


@task
def init(ctx, version=None):
    """ Initialize the RAPyDo framework on your machine """

    raise NotImplementedError("To be completed")

    # # 1. COMPONENTS
    # cycles.tools(ctx, initialize_tool)
    # 2. PROJECTS
    cycles.projects(ctx, initialize_project, init=True)
    # 3. COMMAND LINE TOOLS
    # cycles.cli(ctx, initialize_cli)
    pass
