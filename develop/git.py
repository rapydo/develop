# -*- coding: utf-8 -*-

from develop import execution as exe
from utilities.logs import get_logger

log = get_logger(__name__)


def current_branch():

    cmd = 'git symbolic-ref --short HEAD'
    # cmd = 'git rev-parse --abbrev-ref HEAD'
    return exe.command(cmd)


def checkout(branch, project_name):

    # check git status
    current_branch = None
    existing = False

    for branch_line in exe.command('git branch').split('\n'):
        investigated_branch = branch_line.strip()

        if investigated_branch.startswith('*'):
            investigated_branch = investigated_branch.lstrip('*').lstrip()
            current_branch = investigated_branch

        if investigated_branch == branch:
            existing = True

    # do the right git selection
    if existing:
        if current_branch == branch:
            log.debug('%s already in %s' % (project_name, branch))
            pass
        else:
            out = exe.command('git checkout ' + branch)
            log.debug('switch %s to %s' % (project_name, branch))
            print(out)
    else:
        out = exe.command('git checkout -b ' + branch)
        log.info('created %s in %s' % (branch, project_name))
        print(out)


def push(branch, message=None):

    string = 'nothing to commit'
    if string not in exe.command('git status'):
        if message is None:
            message = "version: %s" % branch
        # exe.command("git add -A")
        exe.command("git commit -a -m '%s'" % message)
        log.warning('Committed missing files')
    else:
        log.very_verbose(string.capitalize())

    gitout = exe.command('git push origin %s' % branch)
    if 'Everything up-to-date' not in gitout:
        log.info('Pushed to remote')
    else:
        log.verbose('Nothing to push')


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
