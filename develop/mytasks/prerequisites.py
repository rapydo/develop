# -*- coding: utf-8 -*-

from invoke import task
from develop import path
from develop import checks
# from utilities.globals import mem
from utilities.logs import get_logger

log = get_logger(__name__)

# # hack for check logs as info
# mem.action = 'check'

######################
# checks
python_cmd = 'python3'
pip_cmd = 'pip3'
twine_cmd = 'twine'
setup_file = 'setup.py'
rc_file = '.pypirc'

pip_check = {
    'type': 'program',
    # 'func': lambda: execution.get_version(pip_cmd, get_result=True),
    'name': pip_cmd,
}

python_check = {
    'type': 'program',
    'name': python_cmd
}

setup_check = {
    'type': 'file',
    'func': lambda: path.build(setup_file).exists(),
    'name': setup_file,
}

twine_check = {
    'type': 'program',
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
        python_check,
        setup_check,
        pip_check
    ])


@task
def release(ctx):
    """ Do necessary things already exist? """

    checklist = [
        python_check,
        setup_check,
        twine_check,
        twinerc_check
    ]

    checks.all(checklist)
