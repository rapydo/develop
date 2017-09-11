# -*- coding: utf-8 -*-

from invoke import Collection  # , Config
from develop import __version__
from develop.program import CLIProgram
from develop.mytasks import \
    package as package_ops, \
    release as release_ops

log = CLIProgram.setup_logger()

# class DoConfig(Config):
#     prefix = 'cmd'
#     # env_prefix = 'TEST'


# Using namespaces for sub-sub commands
ns = Collection()
# ns.add_task()
ns.add_collection(package_ops)
ns.add_collection(release_ops)
program = CLIProgram(namespace=ns, version=__version__)
log.very_verbose("App: %s", program)
