# -*- coding: utf-8 -*-

from invoke import task
from develop import execution
from develop import path
from develop import checks
from utilities.globals import mem
from utilities.logs import get_logger

log = get_logger(__name__)

# hack for check as info
mem.action = 'check'

######################
# checks
pip_cmd = 'pip3'
setup_file = 'setup.py'
twine_cmd = 'twine'
rc_file = '.pypirc'

pip_check = {
    'type': 'program',
    'func': lambda: execution.get_version(pip_cmd, get_result=True),
    'name': pip_cmd,
}

setup_check = {
    'type': 'file',
    'func': lambda: path.build(setup_file).exists(),
    'name': setup_file,
}

twine_check = {
    'type': 'program',
    'func': lambda: execution.get_version(twine_cmd, get_result=True),
    'name': twine_cmd,
}

twinerc_check = {
    'type': 'file',
    'func': lambda: path.home(rc_file).exists(),
    'name': '~/' + rc_file,
}


@task
def install(ctx):
    """ Check prerequisites for installing the package """
    checks.all([
        setup_check,
        pip_check
    ])


@task
def release(ctx):
    """ Do necessary things already exist? """

    checklist = [
        setup_check,
        twine_check,
        twinerc_check
    ]

    checks.all(checklist)
