# -*- coding: utf-8 -*-

import re
from invoke import run
from utilities.logs import get_logger

log = get_logger(__name__)


def output(result, output_array=False):

    if result.ok:
        output = result.stdout
        if output_array:
            output = output.splitlines()
        else:
            output = output.strip()
    else:
        log.exit(result.stderr)

    return output


def command(cmdstring, output_array=True, get_result=False):

    result = run(cmdstring, hide=True, warn=True)
    if get_result:
        return result

    return output(result, output_array)


def parse_version(result, original_name, unknown='Unknown'):

    cmd_out = output(result)

    # usually output is: COMMAND version NUMBER.DECIMAL
    regex = r'([^\s]+)\s+[^\s]+\s+([0-9\.]+)'

    pattern = re.compile(regex)
    match = pattern.search(cmd_out)
    if match:
        if match.group(1) == original_name:
            return match.group(2)
    return unknown


def get_version(cmdstring, version_argument='--version', get_result=False):

    result = command(
        '%s %s' % (cmdstring, version_argument),
        get_result=True
    )

    if get_result:
        return result
    else:
        return parse_version(result, cmdstring)
