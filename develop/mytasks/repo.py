# -*- coding: utf-8 -*-

from invoke import task
from develop import execution as exe
from develop import git
from develop import cycles
from utilities.logs import get_logger

log = get_logger(__name__)


@task
def status(ctx, tools=None, commit=False, message=None):
    """ Verify the status of repositories """

    def single_status(toolname, toolpath, version, commit, message):

        # if toolname == 'develop':
        #     print("SKIPPING")
        #     return False

        branch = git.current_branch()
        log.debug("Branch is: %s", branch)
        if branch != version:
            log.exit("Your configuration is using version: %s", version)

        gitout = exe.command('git status')
        ntc = 'nothing to commit'
        if ntc in gitout:
            log.verbose(ntc)
        else:
            if commit:
                if message is None:
                    message = 'Bump: %s' % version
                exe.command('git add -A')
                exe.command('git commit -m "%s"' % message)
                log.warning("Commit of missing data")
            else:
                log.warning("Things to be committed:")
                print(gitout)

    cycles.tools(
        ctx, single_status,
        tools=tools, params={'commit': commit, 'message': message})


@task
def push(ctx, message=None, sleep_time=2, tools=None):
    """ Push git modifications to remote """

    def myfunc(toolname, toolpath, version, message):

        branch = git.current_branch()
        if branch != version:
            log.exit("Your configuration is using version: %s", version)
        if message is None:
            message = 'Bump: %s' % branch
        git.push(branch, message)

        import time
        log.debug('Sleeping: %s seconds', sleep_time)
        time.sleep(sleep_time)

    cycles.tools(ctx, myfunc, params={'message': message}, tools=tools)
