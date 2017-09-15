# -*- coding: utf-8 -*-

from utilities import logs
from develop import config
from utilities import path

log = logs.get_logger(__name__)


def tools(ctx, func, params=None):

    folder = config.get_parameter(ctx, 'main-path', description='Main path')
    toolposix = path.join(folder, 'tools')

    if params is None:
        params = {}

    # for toolname in config.get_parameter(ctx, 'tools', default={}):
    from develop import TOOLS
    for toolname in TOOLS:

        log.info('Tool: %s' % toolname)
        toolpath = path.join(toolposix, toolname)

        with path.cd(toolpath):
            func(toolpath, params)
