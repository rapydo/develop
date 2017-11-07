# -*- coding: utf-8 -*-

from invoke import task
# from develop import execution as exe
from utilities import helpers
from develop import cycles
from develop import git
from utilities.logs import get_logger

log = get_logger(__name__)


def initialize_tool(name, path, version):

    if path.exists():
        log.checked("Found: %s:%s", name, version)
        current = git.current_branch()
        if current != version:
            log.exit("Wrong branch: %s = %s", path, current)
    else:
        log.error("Failed!")


def initialize_project(name, path, version):
    print("TEST", name, path, version)


def initialize_cli(name, path, version):
    pass


@task
def init(ctx, version=None):
    """ Initialize the RAPyDo framework on your machine """

    # 1. COMPONENTS
    cycles.tools(ctx, initialize_tool, init=True)
    print("DEBUG")
    exit(1)
    # 2. PROJECTS
    cycles.projects(ctx, initialize_project, init=True)
    # 3. COMMAND LINE TOOLS
    # cycles.cli(ctx, initialize_cli)
    pass


@task
def remove(ctx):
    # if path.exists():
    #     helpers.ask_yes_or_no(
    #         'Component: %s' % name +
    #         '\nPath %s not existing (or no permissions).\n' % path +
    #         'Do you want me to create it?',
    #         error='Unable to continue.'
    #     )
    #     print("TEST", path)
    #     raise NotImplementedError("to do!")
    pass
