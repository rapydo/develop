
# Things to do


## best practices

- [x] release base
- [x] short + long description rst (Only short)
- [ ] template cookiecutter


## checks

- [ ] internet connection available (from do to utils?)
from utilities import checks
connected = checks.check_internet()
if not connected:
    log.exit('Internet connection unavailable')
else:
    log.checked("Internet connection available")
- [ ] Yes or No with invoke
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


# Done


## travis

- [x] travis login && travis init
- [x] test travis autodeploy with pypi
- [x] squash noprefix
- [x] git pull request from cli
- [x] git cli tag and so auto-release
