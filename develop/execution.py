# -*- coding: utf-8 -*-

import re
from invoke import run
from utilities.logs import get_logger

log = get_logger(__name__)


def output(result, output_array=False, do_not_die=False):

    if result.ok:
        output = result.stdout
        if output_array:
            output = output.splitlines()
        else:
            output = output.strip()
    else:
        error = result.stderr
        if do_not_die:
            return error.strip()
        else:
            log.exit(error)

    return output


def command(cmdstring, output_array=True, get_result=False):

    result = run(cmdstring, hide=True, warn=True)
    if get_result:
        return result

    return output(result, output_array)


def parse_version(result, original_name, unknown='Unknown'):

    cmd_out = output(result, do_not_die=True)

    # usually output is: COMMAND version NUMBER.DECIMAL
    regex_three = r'^([^\s]+)\s+[^\s]+\s+([0-9\.]+)'
    regex_two = r'^([^\s]+)\s+([0-9\.]+)'

    pattern_three = re.compile(regex_three)
    pattern_two = re.compile(regex_two)

    match = pattern_three.search(cmd_out)
    if not match:
        match = pattern_two.search(cmd_out)
    if match:
        if original_name.startswith(match.group(1)):
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
