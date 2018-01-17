# -*- coding: utf-8 -*-

import time
from invoke import task
from develop import execution as exe
from develop import git
from develop import cycles
from utilities.logs import get_logger

log = get_logger(__name__)


def check_branch(version):
    branch = git.current_branch()
    log.debug("Branch is: %s", branch)
    if branch != version:
        log.exit("Your configuration is using version: %s", version)


@task
def status(ctx, tools=None, commit=False, message=None):
    """ Verify the status of repositories """

    def single_status(toolname, toolpath, version, commit, message):

        check_branch(version)

        if git.changed():
            if commit:
                if message is None:
                    message = 'Bump: %s' % version
                exe.command('git add -A')
                exe.command('git commit -m "%s"' % message)
                log.warning("Commit of missing data")
            else:
                log.warning("You have changes to be committed in %s", toolname)
                print(git.status())
        else:
            log.verbose(git.NO_COMMIT.capitalize())

    cycles.tools(
        ctx, single_status,
        tools=tools, params={'commit': commit, 'message': message})


@task
def push(ctx, message=None, sleep_time=2, tools=None):
    """ Push git modifications to remote """

    def myfunc(toolname, toolpath, version, message):

        check_branch(version)

        if message is None:
            message = 'Bump: %s' % version
        git.push(version, message)

        log.debug('Sleeping: %s seconds', sleep_time)
        time.sleep(sleep_time)

    cycles.tools(ctx, myfunc, params={'message': message}, tools=tools)


@task
def pull(ctx, sleep_time=3, tools=None):
    """ Recover updates from remote """

    def myfunc(toolname, toolpath, version):

        check_branch(version)
        git.pull(version)

        log.debug('Sleeping: %s seconds', sleep_time)
        time.sleep(sleep_time)

    cycles.tools(ctx, myfunc, tools=tools)
