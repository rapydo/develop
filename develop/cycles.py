# -*- coding: utf-8 -*-

from utilities import path
from develop import config
from develop import checks
from develop import TOOLS
from utilities import logs

log = logs.get_logger(__name__)


def tools(ctx, func, params=None, tools=None, connect=True, init=False):

    if connect:
        checks.not_connected()

    # Components path
    tools_current_path = config.components_path(ctx)
    check = path.existing(tools_current_path, do_exit=not init)
    if not check:
        path.create(tools_current_path, directory=True)

    # Needs to be used again in the future
    from utilities.globals import mem
    mem.components_path = tools_current_path

    version = config.parameter(ctx, param_name='current-release')
    log.info("*** current version: %s ***", version)

    tools_version_path = path.join(tools_current_path, version)
    check = path.existing(tools_version_path, do_exit=not init)
    if not check:
        path.create(tools_version_path, directory=True)

    if params is None:
        params = {}

    if tools is None:
        tools = TOOLS[:]
    else:
        tools = tools.split(',')

    base_error = 'Failed to apply a function to all tools'

    for toolname in TOOLS:

        if toolname not in tools:
            continue
        # FIXME: do something here when frontend is updated
        elif toolname == 'frontend':
            log.verbose("Skipping %s", toolname.upper())
            continue

        log.info('\t|| TOOL:\t%s' % toolname)
        toolpath = path.join(tools_version_path, toolname)
        log.verbose("Path: %s", toolpath)

        # give error if path does not exist
        check = path.existing(toolpath, do_exit=not init)
        if not check:
            from utilities.configuration import read
            from develop import git
            defaults = read()
            repos = defaults.get('variables', {}).get('repos', {})
            with path.cd(tools_version_path):
                git.clone(url=repos.get(toolname, {}).get('online_url', None))
            with path.cd(toolpath):
                git.checkout(version, toolname, create_if_not_exists=False)

        with path.cd(toolpath):
            try:
                func(toolname, toolpath, version, **params)
            except TypeError as e:
                if 'unexpected keyword argument' in str(e):
                    error = 'Meta-calling not matching the function signature'
                    log.exit("%s.\n%s:\n%s", base_error, error, e)
                else:
                    raise e
            except BaseException as e:
                # log.warning("Failed")
                raise e


def projects(ctx, func, params=None, projects=None, connect=True, init=False):

    if connect:
        checks.not_connected()

    current_path = config.projects_path(ctx)
    check = path.existing(current_path, do_exit=not init)
    if not check:
        path.create(current_path, directory=True)

    rapydo_version = config.parameter(ctx, param_name='current-release')

    if params is None:
        params = {}

    if projects is not None:
        projects = projects.split(',')

    base_error = 'Failed to apply a function to all projects'
    all_projects = config.parameter(ctx, param_name='projects')

    for prj_name, prj_conf in all_projects.items():

        if projects is not None and prj_name not in projects:
            log.debug("Skipping project: %s", prj_name)
            continue

        prj_version = prj_conf.get('branch')
        prj_main_path = path.join(current_path, prj_name)
        check = path.existing(prj_main_path, do_exit=not init)
        if not check:
            path.create(prj_main_path, directory=True)

        prj_version_path = path.join(prj_main_path, prj_version)

        # GIT CLONE
        check = path.existing(prj_version_path, do_exit=not init)
        if not check:
            from develop import git
            with path.cd(prj_main_path):
                git.clone(url=prj_conf.get('repo'), path=prj_version)
            with path.cd(prj_version_path):
                git.checkout(prj_version, prj_name, create_if_not_exists=False)

        log.info('\t|| PROJECT:\t%s/%s' % (prj_name, prj_version))

        with path.cd(prj_version_path):
            try:
                func(prj_name, prj_version_path, prj_version,
                     rapydo_version, **params)
            except TypeError as e:
                if 'unexpected keyword argument' in str(e):
                    error = 'Meta-calling not matching the function signature'
                    log.exit("%s.\n%s:\n%s", base_error, error, e)
                else:
                    raise e
            except BaseException as e:
                # log.warning("Failed")
                raise e


def clis(ctx, func, params=None, clis=None, connect=True, init=False):

    if connect:
        checks.not_connected()

    current_path = config.cli_path(ctx)
    rapydo_version = config.parameter(ctx, param_name='current-release')
    print(current_path, rapydo_version)

    if params is None:
        params = {}

    if clis is not None:
        clis = clis.split(',')

    base_error = 'Failed to apply a function to all clis'
    cli_projects = config.parameter(ctx, param_name='clis', default={})
    print(cli_projects)

    for prj_name, prj_conf in cli_projects.items():

        if clis is not None and prj_name not in projects:
            log.debug("Skipping CLI project: %s", prj_name)
            continue

        prj_version = prj_conf.get('branch')
        prj_path = path.join(current_path, prj_name, prj_version)
        log.info('\t|| PROJECT:\t%s/%s' % (prj_name, prj_version))

        # CHECK PATH AND DO INIT
        if init:
            raise NotImplementedError("To be done")

        with path.cd(prj_path):
            try:
                func(prj_name, prj_path, rapydo_version, prj_version, **params)
            except TypeError as e:
                if 'unexpected keyword argument' in str(e):
                    error = 'Meta-calling not matching the function signature'
                    log.exit("%s.\n%s:\n%s", base_error, error, e)
                else:
                    raise e
            except BaseException as e:
                # log.warning("Failed")
                raise e
