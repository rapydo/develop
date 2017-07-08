# -*- coding: utf-8 -*-

from invoke import task
from develop import execution as exe
from develop.mytasks import prerequisites
from utilities.logs import get_logger

log = get_logger(__name__)


@task(pre=[prerequisites.install])
def install(ctx, editable=False):
    """ Install on the local host package from the current folder """

    output = exe.long_command(
        cmdstring='pip3 install --upgrade --no-cache-dir --editable .',
        parse_strings=[
            'Running',
            'Successfully',
        ]
    )
    log.info("Output:\n%s" % output)


@task(pre=[prerequisites.release])
def release(ctx):
    """ Release on PyPi the package from the current folder """

    # out = exe.command('echo hello world')
    # log.pp(out)
    log.warning("TODO")
