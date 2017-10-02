# -*- coding: utf-8 -*-

import re
from invoke import task
from develop import execution as exe
from develop import git
from develop import cycles
# from develop import config
# from develop.mytasks import prerequisites
from utilities import path
from utilities import helpers
from utilities import GITREPOS_TEAM, PROJECT_CONF_FILENAME
from utilities.myyaml import YAML_EXT, load_yaml_file
from utilities import logs

log = logs.get_logger(__name__)

VERSION_VAR = '__version__'
REQUIREMENTS_VAR = 'build-requirements'
SETUP_VAR = 'setup'
PROJECT_CONF_VAR = 'projects'
CORE_COMPONENT = 'core'
FRONTEND_COMPONENT = 'frontend'
BASE_PROJECT = 'template'


@task
def tag(ctx, tools=None, name=None, message=None, push=False):
    """ Create a tag release and push it if requested """

    def tagging(toolname, toolpath, version, message, name, push):

        # if version is None:
        #     version = git.current_branch()

        if message is None:
            message = 'Automatic tag'

        if name is None:
            if version == 'master':
                log.exit("You must specify a name with version '%s'", version)
            name = 'v' + version

        git.push_and_tags(push, name, version, message)
        #######################

    cycles.tools(
        ctx, tagging, tools=tools,
        params={'name': name, 'message': message, 'push': push}
    )


@task
def pr(ctx, message=None, force=False):
    """ Create pull requests on all tools based on current branch/version """

    CMD_BASE = 'hub pull-request'

    def pull_requesting(toolname, toolpath, version, force, message):

        cmd = CMD_BASE
        if message is None:
            message = 'Automatic pull-request for version "%s"' % version
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

    cycles.tools(
        ctx, pull_requesting,
        params={'message': message, 'force': force}
    )


def find_python_init(toolname, toolpath):
    """ If there is an __init__.py
    it will tell us if this is a python project/package
    """

    # # NOTE: this is already a python path
    # print("PATH", toolpath, type(toolpath))

    # find out if and how many __init__.py are there
    init = '/__init__.py'
    res = list(toolpath.glob('*%s' % init))

    # remove test directories from the list
    if len(res) == 2:
        newres = []
        for pp in res:
            ppstr = str(pp)
            dirname = helpers.latest_dir(ppstr.replace(init, ''))
            if not dirname.startswith('test'):
                newres.append(pp)
        res = newres.copy()

    # Return 'filepath' to the right __init__.py,
    # or None (not a python package, e.g. docker builds)
    # or Exception on anything else

    if len(res) < 1:
        return None

    if len(res) > 1:

        # if more than one: look for the one with the same name
        for pp in res:
            ppstr = str(pp)
            dirname = helpers.latest_dir(ppstr.replace(init, ''))
            if dirname == toolname:
                filepath = ppstr
                break
        else:
            log.exit("Too many python __init__?\nFound: %s", res)
    else:
        filepath = res.pop()

    return filepath


def compile_regexps(re_dict):

    compiled = {}
    for name, regex in re_dict.items():
        compiled[name] = re.compile(regex)

    return compiled


def read_content(filepath):
    with open(filepath) as fh:
        content = fh.read()
    return content


def replace_content(filepath, newcontent):
    with open(filepath, 'w') as fw:
        fw.write(newcontent)
    log.debug('Overwritten: %s', filepath)


def change_version(filepath, branch, rxps):

    # log.very_verbose("Searching %s:\n%s", VERSION_VAR, filepath)
    content = read_content(filepath)
    pattern = rxps.get(VERSION_VAR)
    match = pattern.search(content)

    if match:
        current_version = match.group(1)
    else:
        log.exit('Missing %s in init file', VERSION_VAR)

    if current_version == branch:
        log.checked('Python %s already matching: %s', VERSION_VAR, branch)
    else:
        log.verbose('Current python %s: %s', VERSION_VAR, current_version)
        replace_content(
            filepath,
            pattern.sub("%s = '%s'" % (VERSION_VAR, branch), content)
        )


def change_requirements(filepath, branch, rxps):
    # log.very_verbose("Searching requirements:\n%s", filepath)
    content = read_content(filepath)
    pattern = rxps.get(REQUIREMENTS_VAR)

    # find
    matches = pattern.findall(content)
    if matches:
        newcontent = content[:]

        # replace only if necessary
        for match in matches:
            if match[1] != branch:
                # NOTE: match[0] is 'branch'
                old = match[0] + match[1]
                new = match[0] + branch
                newcontent = newcontent.replace(old, new)
                log.verbose('Fixed requirement: %s', old)
        if newcontent != content:
            replace_content(filepath, newcontent)
        else:
            log.checked('Already updated: %s',
                        helpers.last_dir(filepath, level=2))


def find_package_name(toolpath, branch, rxps):

    setupfiles = list(toolpath.glob('*setup.py'))
    if len(setupfiles) != 1:
        log.exit("Too many setup files:%s", toolpath)

    setupfile = setupfiles.pop()
    content = read_content(setupfile)
    pattern = rxps.get(SETUP_VAR)
    match = pattern.search(content)
    if match:
        package_name = match.group(1).replace('_', '-')
    else:
        log.exit("No package name: %s", setupfile)

    infos = {}
    data = exe.command('pip3 show %s' % package_name, exit=False)
    # Something already installed
    if isinstance(data, str) and len(data) > 0:
        for info in data.split('\n'):
            key, value = info.split(': ')
            infos[key.lower()] = value

        current_version = infos.get('version')
        if current_version == branch:
            log.checked("Package up to date")
        else:
            log.warning("Package NOT up to date: %s", current_version)

        if infos.get('location') == str(toolpath):
            log.checked("Package installed in development mode")

    # Not installed yet
    else:
        log.debug('%s currently NOT installed', package_name)


def change_project_configuration(projpath, branch, rxps):

    paths = 'projects/%s/%s.%s' % ('*', PROJECT_CONF_FILENAME, YAML_EXT)
    KEY = 'rapydo'

    for filepath in projpath.glob(paths):

        content = read_content(filepath)
        conf = load_yaml_file(filepath)
        current_branch = conf.get('project').get(KEY)
        newcontent = None

        if current_branch is None:
            # add: replace project keyword appending "rapydo: version"
            prjkey = 'project:'
            newcontent = content.replace(
                prjkey,
                '%s\n  %s: %s' % (prjkey, KEY, branch))
        else:
            if current_branch == branch:
                log.checked('Configuration already up to date')
            else:
                # modify
                newcontent = content.replace(
                    '%s: %s' % (KEY, current_branch),
                    '%s: %s' % (KEY, branch)
                )

        if newcontent is not None:
            replace_content(filepath, newcontent)


def link_components(project_name, project_path, components_path):
    """ Handling submodules links in projects """

    from utilities import configuration
    is_template = project_name == BASE_PROJECT
    libs = configuration \
        .read(project_name, is_template) \
        .get('variables').get('repos')

    submodulespath = path.join(project_path, 'submodules')
    from utilities import TOOLS as components

    with path.cd(submodulespath):
        for toolname in libs.keys():
            if toolname in [CORE_COMPONENT, FRONTEND_COMPONENT]:
                continue

            if toolname not in components:
                log.verbose("Skipping non-rapydo tools: %s", toolname)
                continue

            link_path = path.join(submodulespath, toolname)
            if not path.file_exists_and_nonzero(link_path, accept_link=True):
                linked_path = path.join(components_path, toolname)
                exe.command('ln -s %s %s' % (linked_path, link_path))
                log.debug('Linked: %s', linked_path)
            else:
                log.checked('Already linked: %s', toolname)


def switch_project(prj_name, prj_path, prj_version, rapydo_version, rxps):

    change_project_configuration(prj_path, rapydo_version, rxps)

    for req_path in prj_path.glob('projects/*/requirements.txt'):
        change_requirements(req_path, rapydo_version, rxps)

    components_path = helpers.parent_dir(prj_path)
    link_components(prj_name, prj_path, components_path)


@task
def version(ctx, projects=None, push=False, message=None):
    """ Change current release version on all tools """

    # FIXME: decide if use or not push+message

    def versioning(toolname, toolpath, version, push, message, rxps):

        # Switch to the specified branch/version
        git.checkout(version, toolname)

        # Look for the branch version in __init__.py files
        init_path = find_python_init(toolname, toolpath)
        if init_path is None:

            # CORE component
            if toolname == CORE_COMPONENT:
                switch_project(BASE_PROJECT, toolpath, version, version, rxps)
            # BUILDS component
            else:
                for req_path in toolpath.glob('*/*requirements.txt'):
                    change_requirements(req_path, version, rxps)
        # OTHER components/packages
        else:
            change_version(init_path, version, rxps)
            for req_path in toolpath.glob('*requirements.txt'):
                change_requirements(req_path, version, rxps)
            # all but rapydo-http could/should be installed in development mode
            if toolname not in ['http']:
                find_package_name(toolpath, version, rxps)

    ##########################

    rxps = compile_regexps({
        VERSION_VAR: VERSION_VAR + r"\s?=\s?'([0-9\.]+)'",
        REQUIREMENTS_VAR: r'(' + GITREPOS_TEAM + r'/[^@]+@)([a-z0-9-.]+)',
        SETUP_VAR: SETUP_VAR + r"[^a-z]+name='([^\']+)'",
        # PROJECT_CONF_VAR: r'(branch:[\s]+)([a-z0-9-.]+)',
        PROJECT_CONF_VAR: r'([a-z-_]+)\:[\s]+branch\:[\s]([^\s]+)'

    })

    # Take care of all components
    cycles.tools(
        ctx, versioning,
        params={'rxps': rxps, 'push': push, 'message': message},
        connect=push
    )

    # Take care of specified projects
    cycles.projects(
        ctx, switch_project,
        projects=projects, params={'rxps': rxps}, connect=push
    )

# END of FILE
