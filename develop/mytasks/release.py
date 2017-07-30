# -*- coding: utf-8 -*-

from invoke import task
# from develop.mytasks import prerequisites
from develop import execution as exe
from utilities.logs import get_logger

log = get_logger(__name__)


# @task(pre=[prerequisites.install])
@task
def version(ctx, project='core', branch='master'):
    """ Change current release version on all tools """

    # TODO: make the config get a function in `config.py`
    # log.info(ctx.config)
    folder = ctx.config.get('develop', {}).get('tools', {}).get('path')
    log.warning(folder)

    # TODO: refactor this piece of code
    from utilities import path
    from utilities import helpers
    p = path.build(folder)
    # print(list(p.glob('**/*.py')))
    for toolpath in p.iterdir():
        # print(toolpath)
        with path.cd(toolpath):
            out = exe.command('git checkout ' + branch)
            log.debug(
                'switching %s to %s'
                % (helpers.last_dir(toolpath), branch)
            )
            print(out)
