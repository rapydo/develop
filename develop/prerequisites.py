# -*- coding: utf-8 -*-

from invoke import task
from develop import execution
from develop import path
from develop import checks
from utilities.logs import get_logger

log = get_logger(__name__)


@task
def install(ctx):
    """ Check prerequisites for installing the package """
    pass


@task
def release(ctx):
    """ Do necessary things already exist? """

    # # hack for check as info
    # from utilities.globals import mem
    # mem.action = 'check'

    setup_file = 'setup.py'
    cmd = 'twine'
    rc_file = '.pypirc'

    checklist = [
        {
            'type': 'file',
            'func': lambda: path.build(setup_file).exists(),
            'name': setup_file,
        },
        {
            'type': 'program',
            'func': lambda: execution.get_version(cmd, get_result=True),
            'name': cmd,
        },
        {
            'type': 'file',
            'func': lambda: path.home(rc_file).exists(),
            'name': '~/' + rc_file,
        }
    ]

    checks.all(checklist)
