# -*- coding: utf-8 -*-

import better_exceptions as be
from develop.program import CLIProgram
from develop import __version__
from invoke import Collection
from develop.mytasks import \
    package as package_ops, \
    release as release_ops

log = CLIProgram.setup_logger()

ns = Collection()
# ns.add_task()
ns.add_collection(package_ops)
ns.add_collection(release_ops)

program = CLIProgram(namespace=ns, version=__version__)
log.very_verbose("App: %s (+%s)", program, be.__name__)
