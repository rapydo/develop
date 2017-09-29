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


@task
def init(ctx, version=None):
    """ Initialize the RAPyDo framework on your machine """

    def initialize(toolname, toolpath, version):

        if not toolpath.exists():
            helpers.ask_yes_or_no(
                'Component: %s' % toolname +
                '\nPath %s not existing (or no permissions).\n' % toolpath +
                'Do you want me to create it?',
                error='Unable to continue.'
            )
            print("TEST", toolpath)
            raise NotImplementedError("to do!")
            exit(1)
        else:
            log.checked("Found")

    # 1. COMPONENTS
    cycles.tools(ctx, initialize)

    # 2. PROJECTS?
    pass

    # 3. COMMAND LINE TOOLS?
    pass
