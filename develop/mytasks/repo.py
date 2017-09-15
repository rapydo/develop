# -*- coding: utf-8 -*-

from invoke import task
from develop import execution as exe
from develop import cycles
from utilities.logs import get_logger

log = get_logger(__name__)


@task
def status(ctx, tool=None):
    """ Verify the status of the git repositoy of every tool """

    if tool is not None:
        log.exit("Implement only for %s", tool)

    def myfunc(toolpath):
        gitout = exe.command('git status')
        if 'nothing to commit' in gitout:
            pass
        else:
            log.warning("Things to be committed:")
            print(gitout)

    cycles.tools(ctx, myfunc)


@task
def push(ctx, message=None):
    """ Verify the status of the git repositoy of every tool """

    sleep_time = 5

    def myfunc(toolpath, params):

        from develop import git
        branch = git.current_branch()
        message = params.get('message')
        if message is None:
            message = 'Bump: %s' % branch
        git.push(branch, message)

        import time
        time.sleep(sleep_time)

    cycles.tools(ctx, myfunc, {'message': message})
