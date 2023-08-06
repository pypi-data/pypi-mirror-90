[![Build Status](https://api.travis-ci.com/DavidCain/mitoc-const.svg?branch=master)](https://travis-ci.com/DavidCain/mitoc-const/)
[![PyPI version](https://img.shields.io/pypi/v/mitoc-const.svg)](https://pypi.python.org/pypi/mitoc-const)
[![npm version](https://img.shields.io/npm/v/@mitoc/constants.svg)](https://www.npmjs.com/package/@mitoc/constants)

# MITOC Constants
This is a set of constants for use across MIT Outing Club infrastructure.

MITOC has a number of projects, many of which reference values used
in other databases or deployed projects. These projects may be deployed
separately, so there's value in having shared values at constants in an
external package.

## Releasing a new version
It's recommended to keep the Python and TypeScript versions in lock-step.
Even if no changes were made in one of the two, it's best to release both
at the same time.

### pypi/Python
First, augment the version in `setup.py`. Then:

```bash
rm -rf dist/ build/ mitoc_const.egg-info/
pipenv run python setup.py sdist bdist_wheel
pipenv run twine upload dist/*
git push origin master
```

### npm/TypeScript
(Not used yet anywhere, an early prototype)
```bash
npm run build
npm publish
```


## TODO:
- [ ] Add a Makefile for this project:
    - `make lint`, `make test`, and `make check`
    - `make push`
- [ ] Black & isort
- [ ] Run mypy as part of build check
- [ ] Switch to poetry
- [ ] Clean up the (unused) TypeScript package, verify for use
- [ ] Automatically deploy after successful build
