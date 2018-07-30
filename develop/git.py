# -*- coding: utf-8 -*-

from develop import execution as exe
from utilities.logs import get_logger

log = get_logger(__name__)

NO_COMMIT = 'nothing to commit'
MAIN = 'master'


def current_branch():

    cmd = 'git symbolic-ref --short HEAD'
    # cmd = 'git rev-parse --abbrev-ref HEAD'
    return exe.command(cmd)


def clone(url, path=None):

    cmd = 'git clone ' + url
    if path is not None:
        cmd += ' ' + path
    return exe.command(cmd)


def checkout(branch, project_name, create_if_not_exists=True):

    # check git status
    current_branch = None
    existing = False

    exe.command('git fetch')
    for line in exe.command('git branch -a').split('\n'):
        investigated_branch = line.strip().replace('remotes/origin/', '')

        if investigated_branch.startswith('*'):
            investigated_branch = investigated_branch.lstrip('*').lstrip()
            current_branch = investigated_branch

        if investigated_branch == branch:
            existing = True

    # do the right git selection
    if existing:
        if current_branch == branch:
            log.debug('%s already in %s' % (project_name, branch))
        else:
            out = exe.command('git checkout ' + branch)
            log.debug('switch %s to %s' % (project_name, branch))
            print(out)
    else:
        if create_if_not_exists:
            out = exe.command('git checkout -b ' + branch)
            log.info('created %s in %s' % (branch, project_name))
            print(out)
        else:
            log.exit("Branch does not exist: %s", branch)


def status():
    return exe.command('git status')


def changed():
    return NO_COMMIT not in status()


def push(branch, message=None):

    if changed():
        if message is None:
            message = "version: %s" % branch
        # exe.command("git add -A")
        exe.command("git commit -a -m '%s'" % message)
        log.warning('Committed missing files')
    else:
        log.very_verbose(NO_COMMIT.capitalize())

    gitout = exe.command('git push origin %s' % branch)
    if 'Everything up-to-date' not in gitout:
        log.info('Pushed to remote')
    else:
        log.verbose('Nothing to push')


def pull(branch):
    log.debug("Check and download an update")
    gitout = exe.command('git pull origin %s' % branch)
    if gitout.startswith('Already up-to-date'):
        log.debug('Nothing to pull')
    else:
        log.info("Received updates")


def tags():
    return exe.command('git tag --list').split('\n')


def tag(tag_name, branch, message=None, push_decision=False):

    if branch not in tag_name:
        log.exit("Misleading tag %s: not containing %s" % (tag_name, branch))

    import re
    pattern = re.compile(r'^v[0-9.]+$')
    if not pattern.match(tag_name):
        log.exit("Tag accepted for releases are in the form of: vX.Y.Z")

    if tag_name in tags():
        log.debug('Tag %s already exists' % tag_name)
    else:
        # create tag
        exe.command("git tag -a %s -m '%s'" % (tag_name, message))
        log.info("Tagged: %s" % tag_name)
        if push_decision:
            com = "git push origin --follow-tags refs/tags/%s" % tag_name
            exe.command(com)
            log.warning("Pushed tag: %s" % tag_name)


def push_and_tags(push_var, tag_name, branch, message):

    if push_var:
        push(branch, message)

    if tag_name is not None:
        tag(tag_name, branch, message, push_var)
