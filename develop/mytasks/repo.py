# -*- coding: utf-8 -*-

from invoke import task
from develop import execution as exe
from develop import git
from develop import cycles
from utilities.logs import get_logger

log = get_logger(__name__)


@task
def status(ctx, tools=None):
    """ Verify the status of repositories """

    def myfunc(toolpath, params=None):
        gitout = exe.command('git status')
        branch = git.current_branch()
        log.debug("Branch is: %s", branch)
        if 'nothing to commit' in gitout:
            pass
        else:
            log.warning("Things to be committed:")
            print(gitout)

    cycles.tools(ctx, myfunc, tools=tools)


@task
def push(ctx, message=None, sleep_time=2, tools=None):
    """ Push git modifications to remote """

    def myfunc(toolpath, message):

        branch = git.current_branch()
        if message is None:
            message = 'Bump: %s' % branch
        git.push(branch, message)

        import time
        log.debug('Sleeping: %s seconds', sleep_time)
        time.sleep(sleep_time)

    cycles.tools(ctx, myfunc, params={'message': message}, tools=tools)
