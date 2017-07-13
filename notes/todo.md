
# Things to do


## checks

- [ ] long destriction rst and setuptools
- [ ] internet connection available (from do to utils?)
from rapydo.utils import checks
connected = checks.check_internet()
if not connected:
    log.exit('Internet connection unavailable')
else:
    log.checked("Internet connection available")
- [ ] Yes or No with invoke
- [ ] Fix problems if check fails?


## travis

- [x] test travis autodeploy with pypi
- [ ] squash noprefix
- [ ] git pull request from cli
- [ ] git cli tag and so auto-release
- [ ] travis login && travis init


## more

- [ ] Yaml e py check ascii error
- [ ] unittext mocking context
- [ ] git tags = github releases
- [ ] remove 'make' for every packaging project
- [ ] template cli w/ @cookiecutter
- [ ] md posts @blog


## release steps

- [ ] 1. version +1
- [ ] 2. git tag
- [ ] 3. git add commit with message with bump version
- [ ] 4. git push: activate travis build

on travis:

- [ ] 1. convert markdown to rst
    + requires pandoc (ask if they want to install?)
    + option to skip
- [ ] 2. sdist to create package
- [ ] 3. twine register/upload


```
# tree
development/
    tools/
        controller
        utilities
        restapi
        build-templates @onlytags
    eudat/
        submodules
            links
```

