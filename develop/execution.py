# -*- coding: utf-8 -*-

import re
from invoke import run
from utilities.logs import get_logger

log = get_logger(__name__)


def output(result, output_array=False, do_not_die=False):

    if result.ok:
        output = result.stdout.strip()
        if output == '':
            output = result.stderr.strip()
    else:
        error = result.stderr.strip()
        if error == '':
            error = result.stdout.strip()
        if do_not_die:
            output = error
        else:
            log.exit(error)

    if output_array:
        output = output.splitlines()
    else:
        pass

    return output


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
        if original_name.lower().startswith(match.group(1).lower()):
            return match.group(2)
    return unknown


def command(cmdstring, output_array=False, get_result=False, exit=True):
    """
    Execute a 'normal' command based on invoke runners
    """

    result = run(cmdstring, hide=True, warn=True)
    if get_result:
        return result

    return output(result, output_array, do_not_die=not exit)


def get_version(cmdstring, version_argument='--version', get_result=False):

    result = command(
        '%s %s' % (cmdstring, version_argument),
        get_result=True
    )

    if get_result:
        return result
    else:
        return parse_version(result, cmdstring)


def grep_output(result, parse_list):

    lines = output(result, output_array=True, do_not_die=True)
    parsed = []
    for line in lines:
        for catch in parse_list:
            if catch in line:
                parsed.append(line.strip())

    # TODO: check for errors?

    # If nothing catched, return all
    if len(parsed) < 1:
        parsed = lines
    # Join what we recovered
    return '\n'.join(parsed)


def long_command(cmdstring, parse_strings=[]):
    """
    Refactor execution of a serious long command into execution
    - warn user of a long task to wait
    - parse output for a keyword (or regexp in the future)
    """

    log.warning("running 'long' command")
    result = command(cmdstring, get_result=True)

    if len(parse_strings) > 0:
        return grep_output(result, parse_strings)
    else:
        return result
