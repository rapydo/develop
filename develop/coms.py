# -*- coding: utf-8 -*-

"""

TODO: evaluate BONOBO
# graph = bonobo.Graph(extract, transform, load)

"""

from invoke import task
from develop import execution
from develop import prerequisites
from utilities.logs import get_logger

log = get_logger(__name__)


@task(pre=[prerequisites.release])
def package_release(ctx):
    """ Release the package in the current folder """

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


@task(pre=[prerequisites.install])
def package_install(ctx, editable=False):
    """ Install the package locally """

    # cmd = 'pip3 install --upgrade --no-cache-dir --editable .'
    pass
