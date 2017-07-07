# -*- coding: utf-8 -*-

from develop import execution
from utilities.logs import get_logger

log = get_logger(__name__)
checked = log.checked_simple
exit = log.exit


def check_file(obj, objname):
    if obj:
        checked('File: %s' % objname)
    else:
        exit('Missing %s' % objname)


def check_program(obj, objname):
    version = execution.parse_version(obj, objname)
    if obj.ok:
        checked('Program: %s[%s]' % (objname, version))
    else:
        exit('Missing %s' % objname)


def all(checklist):

    for op in checklist:

        optype = op.get('type')
        objname = op.get('name')
        obj = op.get('func')()

        if optype == 'file':
            check_file(obj, objname)
        elif optype == 'program':
            check_program(obj, objname)
