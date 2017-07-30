
# Things to do

set the root path with a `.developrc` file, then:

```
# tree
development/
    tools/
        controller
        utilities
        restapi
        build-templates @onlytags
    projects/
        core/
            submodules
                links
        eudat/
            submodules
                links
```


## switch version

- list tools:
    + builds, controller, develop, http, utilities
    + read from projects_defaults ?
- list projects from dir:
    + core, eudat, others 
- dependencies:
    + utils > develop > core > controller > build-templates > http

- choose: project e.g. 'eudat' AND branch e.g. '0.5.3'
- for each `tools`
    - glob/pathlib on */__init__.py and change __version__.py
        - use regexps and expressions
    - change projects/eudat/project_configuration.yaml
        - YAML path is repos: utils, backend and build-templates
    - git branch -a
        - if exists: git checkout $BRANCH
        - else create: git checkout -b $BRANCH
            + and push
    - pip3 install editable/develop


## best practices

- [ ] template cookiecutter


## checks

- [ ] Yes or No with invoke
- [ ] internet connection available (from do to utils?)
from utilities import checks
connected = checks.check_internet()
if not connected:
    log.exit('Internet connection unavailable')
else:
    log.checked("Internet connection available")
- [ ] Fix problems if check fails?


## more

- [x] git tags = github releases
- [ ] Yaml e py check ascii error
- [ ] spinner + gauge = py-clui
- [ ] remove 'make' for every packaging project
- [ ] template cli w/ @cookiecutter
- [ ] md posts @blog


## release steps

- [ ] 1. version +1
- [ ] 2. git tag
- [ ] 3. git add commit with message with bump version
- [ ] 4. git push: activate travis build


# Done

- [x] travis login && travis init
- [x] test travis autodeploy with pypi
- [x] squash noprefix
- [x] git pull request from cli
- [x] git cli tag and so auto-release
- [x] release base
- [x] short + long description rst (Only short)
