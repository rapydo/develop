# -*- coding: utf-8 -*-

from develop import execution
from develop import path
from utilities.logs import get_logger

log = get_logger(__name__)
checked = log.checked_simple
fail = log.fail
critical = log.critical
exit = log.critical_exit


def not_found(error, check_path=False):
    fail(error)
    if check_path:
        critical(
            'Things were not found.' +
            '\nPlease consider checking current path:\n' +
            '%s' % path.current()
        )
    exit()


def check_file(obj, objname):
    if obj:
        checked('File: %s' % objname)
    else:
        not_found('Missing file "%s"' % objname, check_path=True)


def check_program(obj, objname):
    version = execution.parse_version(obj, objname)
    if obj.ok:
        checked('Program: %s [v%s]' % (objname, version))
    else:
        not_found('Missing executable "%s"' % objname)


def all(checklist):

    for op in checklist:

        optype = op.get('type')
        objname = op.get('name')
        obj = op.get('func')()

        if optype == 'file':
            check_file(obj, objname)
        elif optype == 'program':
            check_program(obj, objname)
