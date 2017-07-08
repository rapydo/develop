# -*- coding: utf-8 -*-

from invoke import task
from develop import execution
from develop.mytasks import prerequisites
from utilities.logs import get_logger

log = get_logger(__name__)


@task(pre=[prerequisites.install])
def install(ctx, editable=False):
    """ Install on the local host package from the current folder """

    cmd = 'pip3 install --upgrade --no-cache-dir --editable .'
    log.debug(cmd)
    # out = execution.command(cmd)
    pass


@task(pre=[prerequisites.release])
def release(ctx):
    """ Release on PyPi the package from the current folder """

    out = execution.command('echo hello world')
    log.pp(out)

    # . build with setup.py
    #   - check if already builded
    # . get package version
    # . twine register
    # . git
    #   - add
    #   - commit with message
    #   - push

    log.info("Completed")
