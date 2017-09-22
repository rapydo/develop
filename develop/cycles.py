# -*- coding: utf-8 -*-

from utilities import path
from develop import config
from develop import TOOLS
from utilities import logs

log = logs.get_logger(__name__)


def tools(ctx, func, params=None, tools=None):

    tools_current_path = config.components_path(ctx)

    if params is None:
        params = {}

    if tools is None:
        tools = TOOLS[:]

    for toolname in TOOLS:

        if toolname not in tools:
            continue

        log.info('Tool: %s' % toolname)
        toolpath = path.join(tools_current_path, toolname)
        log.verbose("Path: %s", toolpath)

        with path.cd(toolpath):
            func(toolpath, params)
