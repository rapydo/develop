# -*- coding: utf-8 -*-

import better_exceptions as be
from utilities.cli import App
from develop import __version__
from invoke import Collection
from develop.mytasks import package, release, repo, framework
from develop.mytasks.init import init

log = App.setup_logger(name=__name__)

ns = Collection()
ns.add_task(init)
ns.add_collection(framework)
ns.add_collection(package)
ns.add_collection(release)
ns.add_collection(repo)

program = App(namespace=ns, version=__version__)
log.very_verbose("App: %s (+%s)", program, be.__name__)
