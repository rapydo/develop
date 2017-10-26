# -*- coding: utf-8 -*-

from invoke import task
from develop import execution as exe
from develop.mytasks import prerequisites
# from develop import cycles
from utilities.logs import get_logger

log = get_logger(__name__)


@task(pre=[prerequisites.install])
def install(ctx, editable=False):
    """ Install on the local host package from the current folder """

    # FIXME: cycle and apply to work with utilities, controller and develop
    # raise NotImplementedError("to be completed")

    output = exe.long_command(
        cmdstring='pip3 install --upgrade --no-cache-dir --editable .',
        parse_strings=[
            'Running',
            'Successfully',
        ]
    )
    log.info("Completed w/ output:\n%s" % output)


# @task(pre=[prerequisites.release])
# def release(ctx):
#     """ Release on PyPi the package from the current folder """

#     out = exe.command('echo hello world')
#     log.debug(show_release_output(out))
#     log.warning("TODO")


def show_release_output(raw):
    return raw
