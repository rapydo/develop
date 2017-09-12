# -*- coding: utf-8 -*-
from utilities.logs import get_logger

log = get_logger(__name__)


def get_parameter(ctx, param_name, default=None, description=None):

    config = ctx.config.get('develop', {})
    param_value = config.get(param_name, default)
    if param_value is None:
        log.exit("Missing %s definition in ~/.invoke.yaml" % param_name)
    else:
        if description is None:
            description = 'Param ' + param_name
        log.debug("%s: %s" % (description, param_value))

    return param_value
