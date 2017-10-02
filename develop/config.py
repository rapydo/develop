# -*- coding: utf-8 -*-

from utilities import path
from utilities.logs import get_logger

log = get_logger(__name__)


def parameters_value(ctx):
    return ctx.config.get('develop', {})


def parameter(ctx, param_name, default=None, description=None):

    all_config = parameters_value(ctx)
    param_value = all_config.get(param_name, default)

    if param_value is None:
        log.exit("Missing parameter '%s' definition " +
                 "in ~/.invoke.yaml", param_name)
    else:
        if description is None:
            description = 'Param ' + param_name
        log.verbose("%s: %s" % (description, param_value))

    return param_value


def main_path(ctx):
    # folder = config.parameter(ctx, 'main-path', description='Main path')
    return path.build(
        parameter(
            ctx, param_name='path', default='/tmp',
            description='Main path for development of rapydo'
        )
    )


def components_path(ctx):
    return path.join(main_path(ctx), 'components')


def projects_path(ctx):
    return path.join(main_path(ctx), 'projects')


def cli_path(ctx):
    return path.join(main_path(ctx), 'cli')
