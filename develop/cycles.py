# -*- coding: utf-8 -*-

from utilities import path
from develop import config
from develop import checks
from develop import TOOLS
from utilities import logs

log = logs.get_logger(__name__)


def tools(ctx, func, params=None, tools=None, check_connection=True):

    if check_connection:
        checks.not_connected()

    tools_current_path = config.components_path(ctx)

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

        log.info('Tool: %s' % toolname)
        toolpath = path.join(tools_current_path, toolname)
        log.verbose("Path: %s", toolpath)

        with path.cd(toolpath):
            try:
                func(toolpath, **params)
            except TypeError as e:
                if 'unexpected keyword argument' in str(e):
                    error = 'Meta-calling not matching the function signature'
                    log.exit("%s.\n%s:\n%s", base_error, error, e)
                else:
                    raise e
            except BaseException as e:
                # log.warning("Failed")
                raise e
