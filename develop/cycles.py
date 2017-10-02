# -*- coding: utf-8 -*-

from utilities import path
from develop import config
from develop import checks
from utilities import TOOLS
from utilities import logs

log = logs.get_logger(__name__)


def tools(ctx, func, params=None, tools=None, connect=True, init=False):

    if connect:
        checks.not_connected()

    tools_current_path = config.components_path(ctx)
    version = config.parameter(ctx, param_name='current-release')

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

        # print()
        log.info('\t|| TOOL:\t%s ||' % toolname)
        toolpath = path.join(tools_current_path, version, toolname)
        log.verbose("Path: %s", toolpath)

        # FIXME: check for the path

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
        # checks.not_connected()
        pass

    current_path = config.projects_path(ctx)
    # rapydo_version = config.parameter(ctx, param_name='current-release')

    if params is None:
        params = {}

    if projects is not None:
        projects = projects.split(',')

    # base_error = 'Failed to apply a function to all projects'
    all_projects = config.parameter(ctx, param_name='projects')

    for prj_name, prj_conf in all_projects.items():

        if projects is not None and prj_name not in projects:
            continue

        prj_version = prj_conf.get('branch')
        prj_path = path.join(current_path, prj_name, prj_version)

        # CHECK PATH AND DO INIT
        if init:
            print("PEPPE")
            pass

        with path.cd(prj_path):
            print("TEST DIR", prj_path)
