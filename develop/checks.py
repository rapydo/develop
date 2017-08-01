# -*- coding: utf-8 -*-

from develop import execution
from utilities import path
from utilities import checks
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


def not_connected():
    if not checks.internet_connection_available():
        log.exit('Internet connection unavailable')
    else:
        log.checked("Internet connection available")


def check_file(func, objname):
    if func():
        checked('File: %s' % objname)
    else:
        not_found('Missing file "%s"' % objname, check_path=True)


def check_program(objname):
    obj = execution.get_version(objname, get_result=True)
    if obj.ok:
        version = execution.parse_version(obj, objname)
        checked('Program: %s [v%s]' % (objname, version))
    else:
        not_found('Missing executable "%s"' % objname)


def all(checklist):

    for op in checklist:

        optype = op.get('type')
        objname = op.get('name')

        if optype == 'file':
            check_file(op.get('func'), objname)
        elif optype == 'program':
            check_program(objname)
