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
    if folder is None:
        log.exit("Missing folder definition in ~/.invoke.yaml")
    else:
        log.verbose("Main path: %s" % folder)

    # TODO: refactor this piece of code
    import re
    from utilities import path
    from utilities import helpers
    p = path.build(folder)

    for toolpath in p.iterdir():

        toolname = helpers.last_dir(toolpath)
        log.debug('Tool: %s' % toolname)

        with path.cd(toolpath):

            # check git status
            current = None
            existing = False
            for branch_line in exe.command('git branch').split('\n'):
                mybranch = branch_line.strip()

                if mybranch.startswith('*'):
                    mybranch = mybranch.lstrip('*').lstrip()
                    current = mybranch

                if mybranch == branch:
                    existing = True

            # do the right git selection
            if existing:
                if current == branch:
                    log.verbose('%s already in %s' % (toolname, branch))
                    pass
                else:
                    out = exe.command('git checkout ' + branch)
                    log.debug('switch %s to %s' % (toolname, branch))
                    print(out)
            else:
                out = exe.command('git checkout -b ' + branch)
                log.info('created %s in %s' % (branch, toolname))
                print(out)

            # change __version__
            x = path.build([toolpath])
            res = list(x.glob('**/__init__.py'))
            if len(res) < 1:
                continue
            elif len(res) > 1:
                log.exit("Too many init: %s" % res)
            else:
                filepath = res.pop()

            log.verbose("Searching version:\n%s" % filepath)
            with open(filepath) as fh:
                content = fh.read()

            # re find
            version_re = r"__version__\s?=\s?'([0-9\.]+)'"
            pattern = re.compile(version_re)
            match = pattern.search(content)
            if match:
                version = match.group(1)
            else:
                log.exit('Missing version in init file')

            if version == branch:
                log.verbose('Python version already matching')
            else:
                log.very_verbose('Current python version: %s' % version)
                # re replace

            exit(1)

        # out of CD

    # out of FOR
