# PyProject Script

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/anthonyalmarza/pyscript/branch/main/graph/badge.svg?token=JRCC98L3FG)](https://codecov.io/gh/anthonyalmarza/pyscript)
![Build](https://github.com/anthonyalmarza/pyscript/workflows/Build/badge.svg)

## Overview

`PyProject Script` is a very simple development tool intended to be used with `pyproject.toml` configuration files.
The intention is to provide an interface for running scripts within a local development workflow.

```toml
# in your pyproject.toml
[tool.pyscript]
tests = "path.to.my.tests.script:entrypoint_callable"
```

Running `pyscript tests` after installing `pyscript` will import the `path.to.my.tests.script` module and will call
`entrypoint_callable` callable.

This works in much the same way as `poetry`'s `poetry run` command without actually including those scripts in your
project build.

> NOTE: This is an alpha release. Use it your own risk.

## Installation

`pip install pyproject-script`

or if you're using `poetry`

`poetry add -D pyproject-script`


## Local Development

### Pyenv
It's recommended that you use [`pyenv`](https://github.com/pyenv/pyenv)

[pyenv-installer](https://github.com/pyenv/pyenv-installer)
```bash
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

### Install `poetry`

This project uses [`poetry`](https://python-poetry.org). Install it using the following command.
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
More instructions [here](https://python-poetry.org/docs/#installation)

### Install the dependencies:

`poetry install`

Install pre-commit hooks:

`poetry run pre-commit install`

### Running Tests:

`poetry run pyscript tests`
