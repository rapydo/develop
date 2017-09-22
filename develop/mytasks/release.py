# -*- coding: utf-8 -*-

import re
from invoke import task
from develop import execution as exe
from develop import git
from develop import checks
from develop import cycles
from develop import config
# from develop.mytasks import prerequisites
from utilities import path
from utilities import helpers
from utilities import GITREPOS_TEAM
from utilities import logs

log = logs.get_logger(__name__)


# @task(pre=[prerequisites.install])
@task
def status(ctx):
    """ test """

    folder = config.get_parameter(ctx, 'main-path', description='Main path')
    toolposix = path.join(folder, 'tools')

    for toolname in config.get_parameter(ctx, 'tools', default={}):

        log.info('Tool: %s' % toolname)
        toolpath = path.join(toolposix, toolname)

        with path.cd(toolpath):
            gitout = exe.command('git status')
            if 'nothing to commit' in gitout:
                pass
            else:
                log.warning("Things to be committed:")
                print(gitout)


@task
def tag(ctx):
    """ to do """
    pass


@task
def pr(ctx, message=None, branch='master', force=False):
    """ Create pull requests on all tools based on current branch/version """

    def myfunc(toolpath, params):

        cmd = CMD_BASE

        force = params.get('force')
        branch = params.get('branch')
        message = params.get('message')
        if message is None:
            message = 'Automatic pull request to release version "%s"' % branch

        if force:
            cmd += ' -f'
        cmd += ' -m \"%s\"' % message

        out = exe.command(cmd, exit=False)
        if 'error' in out.lower():
            # NOTE: twice a pull request on the same branch gives error
            if 'pull request already exists for' in out:
                log.warning("Already exists")
            else:
                log.exit("Failed:\n%s", out)
        else:
            log.info("Created pull request: %s", out)

    checks.not_connected()
    CMD_BASE = 'hub pull-request'

    cycles.tools(
        ctx, myfunc, {'message': message, 'branch': branch, 'force': force})


# @task(pre=[prerequisites.install])
@task
def version(ctx,
            project='core', branch='master',
            push=False, tag=None,
            message=None, develop=False):
    """ Change current release version on all tools """

    if push or tag is not None:
        checks.not_connected()

    folder = config.parameter(ctx, 'main-path', description='Main path')

    #######################################
    # TODO: refactor this whole piece of code below
    #######################################
    toolposix = path.join(folder, 'tools')
    installed = False

    for toolname in config.parameter(ctx, 'tools', default={}):

        log.info('Tool: %s', toolname)
        toolpath = path.join(toolposix, toolname)

        with path.cd(toolpath):

            git.checkout(branch, toolname)

            # NOTE: knowing if there is an __init__.py or not
            # will tell us if this is a python project/package
            x = path.build([toolpath])
            init = '/__init__.py'

            # find out if and how many __init__.py are there
            res = list(x.glob('*%s' % init))

            # remove test directories from the list
            if len(res) == 2:
                newres = []
                for pp in res:
                    ppstr = str(pp)
                    dirname = helpers.latest_dir(ppstr.replace(init, ''))
                    if not dirname.startswith('test'):
                        newres.append(pp)
                res = newres.copy()

            if len(res) < 1:
                #######################################
                # it looks like this is not a python package
                # would this be 'build templates'?

                version_re = r'(' + GITREPOS_TEAM + r'/[^@]+@)([a-z0-9-.]+)'
                pattern = re.compile(version_re)

                # find and replace all requirements files
                for req in x.glob('*/*requirements.txt'):

                    # open
                    log.very_verbose("Searching version:\n%s", req)
                    with open(req) as fh:
                        content = fh.read()

                    # find
                    matches = pattern.findall(content)
                    if matches:
                        newcontent = content[:]

                        # replace only if necessary
                        for match in matches:
                            if match[1] != branch:
                                old = match[0] + match[1]
                                new = match[0] + branch
                                newcontent = newcontent.replace(old, new)
                                log.very_verbose('Fixed requirement: %s', old)
                        if newcontent != content:
                            with open(req, 'w') as fw:
                                fw.write(newcontent)
                            log.info('Updated: %s', req)
                        else:
                            log.checked('%s untouched', helpers.last_dir(req))

                git.push_and_tags(push, tag, branch, message)
                continue

            elif len(res) > 1:

                # if more than one: look for the one with the same name
                for pp in res:
                    ppstr = str(pp)
                    dirname = helpers.latest_dir(ppstr.replace(init, ''))
                    if dirname == toolname:
                        filepath = ppstr
                        break
                else:
                    log.exit("Too many init: %s", res)
            else:
                filepath = res.pop()

            # change __version__
            log.very_verbose("Searching version:\n%s", filepath)
            with open(filepath) as fh:
                content = fh.read()

            # re find
            version_var = '__version__'
            version_re = version_var + r"\s?=\s?'([0-9\.]+)'"
            pattern = re.compile(version_re)
            match = pattern.search(content)
            if match:
                version = match.group(1)
            else:
                log.exit('Missing version in init file')

            if version == branch:
                log.checked('Python version already matching')
            # re replace
            else:
                log.very_verbose('Current python version: %s', version)
                new_content = pattern.sub(
                    "%s = '%s'" % (version_var, branch), content)
                with open(filepath, 'w') as fw:
                    fw.write(new_content)
                log.info('Overwritten python version: %s', branch)

            #######################################
            # Python requirements
            version_re = r'(' + GITREPOS_TEAM + r'/[^@]+@)([a-z0-9-.]+)'
            pattern = re.compile(version_re)

            # find and replace all requirements files
            for req in x.glob('*requirements.txt'):
                # open
                log.very_verbose("Searching version:\n%s", req)
                with open(req) as fh:
                    content = fh.read()
                # find
                matches = pattern.findall(content)
                if matches:
                    newcontent = content[:]

                    # replace only if necessary
                    for match in matches:
                        if match[1] != branch:
                            old = match[0] + match[1]
                            new = match[0] + branch
                            newcontent = newcontent.replace(old, new)
                            log.very_verbose('Fixed requirement: %s', old)
                    if newcontent != content:
                        with open(req, 'w') as fw:
                            fw.write(newcontent)
                        log.info('Updated: %s', req)
                    else:
                        log.checked('Requirements already matching')

            if toolname not in ['http']:

                #######################################
                # Python setup.py
                naming_re = r"setup[^a-z]+name='([^\']+)'"
                pattern = re.compile(naming_re)
                setupfile = list(x.glob('*setup.py')).pop()
                with open(setupfile) as fh:
                    content = fh.read()
                match = pattern.search(content)
                if match:
                    package_name = match.group(1).replace('_', '-')

                #######################################
                # install in development mode
                infos = {}
                data = exe.command('pip3 show %s' % package_name, exit=False)
                if isinstance(data, str) and len(data) > 0:
                    for info in data.split('\n'):
                        key, value = info.split(': ')
                        infos[key.lower()] = value
                else:
                    log.verbose('%s currently not installed', package_name)

                doinstall = True
                if infos.get('location') == str(toolpath):
                    if infos.get('version') == version:
                        doinstall = False

                if doinstall:
                    exe.command(
                        'pip3 install --upgrade --no-cache-dir --editable .')
                    installed = True
                    log.warning('installed %s==%s in develop mode',
                                package_name, version)
            else:
                log.info("Skipped installation")

            git.push_and_tags(push, tag, branch, message)

            # exit(1)
            # out of TOOL

        # out of CD

    # out of FOR

    #######################################
    # Core or eudat (project)
    iscore = project == 'core'
    if iscore:
        log.info('PROJECT: core')
        projpath = path.join(folder, project)

        # FIXME: to look for dir names in configuration
        links = {
            'http': 'backend',
            'builds': 'builds_base',
            'utilities': 'utilities'
        }

        submodulespath = path.join(projpath, 'submodules')
        with path.cd(submodulespath):
            for name, link in links.items():
                linkpath = path.join(submodulespath, link)
                if not path.file_exists_and_nonzero(linkpath):
                    toolpath = path.join(toolposix, name)
                    exe.command('ln -s %s %s' % (toolpath, link))
                    log.debug('Linked: %s', toolpath)

        project = 'template'

    #######################################
    else:
        # This is a forked project (e.g. EUDAT)
        folder = config.parameter(
            ctx, 'fork-path', default={}).get(project)
        if folder is None:
            log.exit("Missing fork dir definition in ~/.invoke.yaml")
        projpath = path.build(folder)
        log.info('PROJECT: %s', project)

    #######################################
    # project requirements regex replace
    version_re = r'(' + GITREPOS_TEAM + r'/[^@]+@)([a-z0-9-.]+)'
    pattern = re.compile(version_re)
    for req in projpath.glob('projects/%s/requirements.txt' % project):
        log.very_verbose("Searching in:\n%s", req)
        # open
        with open(req) as fh:
            content = fh.read()
        # find
        matches = pattern.findall(content)
        if matches:
            newcontent = content[:]

            # replace only if necessary
            for match in matches:
                if match[1] != branch:
                    old = match[0] + match[1]
                    new = match[0] + branch
                    newcontent = newcontent.replace(old, new)
                    log.very_verbose('Fixed requirement: %s', old)
            if newcontent != content:
                with open(req, 'w') as fw:
                    fw.write(newcontent)
                log.info('Updated: %s', req)
            else:
                log.checked('Requirements already matching')

    #######################################
    # project configuration regex replace
    version_re = r'(branch:[\s]+)([a-z0-9-.]+)'
    pattern = re.compile(version_re)
    from utilities import PROJECT_CONF_FILENAME
    from utilities.myyaml import YAML_EXT
    filename = 'projects/%s/%s.%s' % (project, PROJECT_CONF_FILENAME, YAML_EXT)
    for req in projpath.glob(filename):
        log.very_verbose("Searching in:\n%s", req)
        # open
        with open(req) as fh:
            content = fh.read()
        # find
        matches = pattern.findall(content)
        if matches:
            newcontent = content[:]
            # replace only if necessary
            for match in matches:
                if match[1] != branch:
                    old = match[0] + match[1]
                    new = match[0] + branch
                    newcontent = newcontent.replace(old, new)
                    log.very_verbose('Fixed requirement: %s', old)
            if newcontent != content:
                with open(req, 'w') as fw:
                    fw.write(newcontent)
                log.info('Updated: %s', req)
            else:
                log.checked('Project Configuration: already matching')

    # Only if a rapydo component
    if iscore:
        with path.cd(projpath):
            git.checkout(branch, 'core')
            git.push_and_tags(push, tag, branch, message)

    if installed:
        out = exe.com('pip3 list --format columns | grep %s' % GITREPOS_TEAM)
        log.warning('Currently installed:\n%s', out)
