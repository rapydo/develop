# -*- coding: utf-8 -*-

from invoke import task
from develop import cycles
from develop import execution as exe
from develop.mytasks import prerequisites
# from develop import cycles
from utilities.logs import get_logger

log = get_logger(__name__)


# @task(pre=[prerequisites.install])
@task
def install(ctx, tools=None):
    """ Install local hosted tools as cli """

    def installer(toolname, toolpath, version):

        # check if this is a python package
        prerequisites.install()

        output = exe.long_command(
            cmdstring='pip3 install --upgrade --no-cache-dir --editable .',
            parse_strings=[
                'Running',
                'Successfully',
            ]
        )
        log.debug("Completed w/ output:\n%s" % output)
        log.info("Locally installed: %s", toolname)

    if tools is None:
        tools = 'utils,develop,do'

    cycles.tools(ctx, installer, tools=tools, params={})


# @task(pre=[prerequisites.release])
# def release(ctx):
#     """ Release on PyPi the package from the current folder """

#     out = exe.command('echo hello world')
#     log.debug(show_release_output(out))
#     log.warning("TODO")


def show_release_output(raw):
    return raw
