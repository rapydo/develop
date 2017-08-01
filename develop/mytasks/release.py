# -*- coding: utf-8 -*-

from invoke import task
# from develop.mytasks import prerequisites
from develop import execution as exe
from utilities import logs

log = logs.get_logger(__name__)
# FIXME: set global level from global option?
log.setLevel(logs.VERBOSE)


def git_checkout(branch, project_name):

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


def git_push(branch, message=None):

    if 'nothing to commit' not in exe.command('git status'):
        if message is None:
            message = "version: %s" % branch
        exe.command("git commit -a -m '%s'" % message)
        log.warning('Committed missing files')

    gitout = exe.command('git push origin %s' % branch)
    if 'Everything up-to-date' not in gitout:
        log.info('Pushed to remote')


# @task(pre=[prerequisites.install])
@task
def version(ctx,
            project='core', branch='master',
            push=False, tag=False, message=None):
    """ Change current release version on all tools """

    if push or tag:
        from utilities import checks
        if not checks.internet_connection_available():
            log.exit('Internet connection unavailable')
        else:
            log.checked("Internet connection available")

    # TODO: make the config get a function in `config.py`
    config = ctx.config.get('develop', {})
    folder = config.get('main-path')
    if folder is None:
        log.exit("Missing folder definition in ~/.invoke.yaml")
    else:
        log.debug("Main path: %s" % folder)

    #######################################
    # TODO: refactor this whole piece of code below
    #######################################
    import re
    from utilities import path
    from utilities import helpers
    from utilities import GITREPOS_TEAM
    toolposix = path.join(folder, 'tools')

    # # FIXME: to look for dir names in configuration
    # for toolpath in toolposix.iterdir():
    #     toolname = helpers.last_dir(toolpath)

    for toolname in config.get('tools'):

        log.info('Tool: %s' % toolname)
        toolpath = path.join(toolposix, toolname)

        with path.cd(toolpath):

            git_checkout(branch, toolname)

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
                    log.very_verbose("Searching version:\n%s" % req)
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
                                log.very_verbose('Fixed requirement: %s' % old)
                        if newcontent != content:
                            with open(req, 'w') as fw:
                                fw.write(newcontent)
                            log.info('Updated: %s' % req)
                        else:
                            log.verbose('%s untouched' % req)

                if push:
                    git_push(branch, message)

                if tag:
                    raise NotImplementedError("tag: check or create and push!")

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
                    log.exit("Too many init: %s" % res)
            else:
                filepath = res.pop()

            # change __version__
            log.very_verbose("Searching version:\n%s" % filepath)
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
                log.very_verbose('Current python version: %s' % version)
                new_content = pattern.sub(
                    "%s = '%s'" % (version_var, branch), content)
                with open(filepath, 'w') as fw:
                    fw.write(new_content)
                log.info('Overwritten python version: %s' % branch)

            #######################################
            # Python requirements
            version_re = r'(' + GITREPOS_TEAM + r'/[^@]+@)([a-z0-9-.]+)'
            pattern = re.compile(version_re)

            # find and replace all requirements files
            for req in x.glob('*requirements.txt'):
                # open
                log.very_verbose("Searching version:\n%s" % req)
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
                            log.very_verbose('Fixed requirement: %s' % old)
                    if newcontent != content:
                        with open(req, 'w') as fw:
                            fw.write(newcontent)
                        log.info('Updated: %s' % req)
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
                data = exe.command('pip3 show %s' % package_name)
                for info in data.split('\n'):
                    key, value = info.split(': ')
                    infos[key.lower()] = value

                doinstall = True
                if infos.get('location') == str(toolpath):
                    if infos.get('version') == version:
                        doinstall = False

                if doinstall:
                    exe.command(
                        'pip3 install --upgrade --no-cache-dir --editable .')
                    log.installed('installed %s==%s in develop mode'
                                  % (package_name, version))
            else:
                log.info("Skipped installation")

            if push:
                git_push(branch, message)

            if tag:
                raise NotImplementedError("git tag check or create and push!")

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
                    log.debug('Linked: %s' % toolpath)

        project = 'template'

    #######################################
    else:
        # This is a forked project (e.g. EUDAT)
        folder = config.get('fork-path', {}).get(project)
        if folder is None:
            log.exit("Missing fork dir definition in ~/.invoke.yaml")
        projpath = path.build(folder)
        log.info('PROJECT: %s' % project)

    #######################################
    # project requirements regex replace
    version_re = r'(' + GITREPOS_TEAM + r'/[^@]+@)([a-z0-9-.]+)'
    pattern = re.compile(version_re)
    for req in projpath.glob('projects/%s/requirements.txt' % project):
        log.very_verbose("Searching in:\n%s" % req)
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
                    log.very_verbose('Fixed requirement: %s' % old)
            if newcontent != content:
                with open(req, 'w') as fw:
                    fw.write(newcontent)
                log.info('Updated: %s' % req)
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
        log.very_verbose("Searching in:\n%s" % req)
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
                    log.very_verbose('Fixed requirement: %s' % old)
            if newcontent != content:
                with open(req, 'w') as fw:
                    fw.write(newcontent)
                log.info('Updated: %s' % req)
            else:
                log.checked('Project Configuration: already matching')

    # Only if a rapydo component
    if iscore:

        git_checkout(branch, 'core')

        if push:
            with path.cd(projpath):
                git_push(branch, message)
