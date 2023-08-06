# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyscript']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pyscript = pyscript.cli:main']}

setup_kwargs = {
    'name': 'pyproject-script',
    'version': '0.0.0a0',
    'description': '',
    'long_description': '# PyProject Script\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![codecov](https://codecov.io/gh/anthonyalmarza/pyscript/branch/main/graph/badge.svg?token=JRCC98L3FG)](https://codecov.io/gh/anthonyalmarza/pyscript)\n![Build](https://github.com/anthonyalmarza/pyscript/workflows/Build/badge.svg)\n\n## Overview\n\n`PyProject Script` is a very simple development tool intended to be used with `pyproject.toml` configuration files.\nThe intention is to provide an interface for running scripts within a local development workflow.\n\n```toml\n# in your pyproject.toml\n[tool.pyscript]\ntests = "path.to.my.tests.script:entrypoint_callable"\n```\n\nRunning `pyscript tests` after installing `pyscript` will import the `path.to.my.tests.script` module and will call\n`entrypoint_callable` callable.\n\nThis works in much the same way as `poetry`\'s `poetry run` command without actually including those scripts in your\nproject build.\n\n> NOTE: This is an alpha release. Use it your own risk.\n\n## Installation\n\n`pip install pyproject-script`\n\nor if you\'re using `poetry`\n\n`poetry add -D pyproject-script`\n\n\n## Local Development\n\n### Pyenv\nIt\'s recommended that you use [`pyenv`](https://github.com/pyenv/pyenv)\n\n[pyenv-installer](https://github.com/pyenv/pyenv-installer)\n```bash\ncurl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash\n```\n\n### Install `poetry`\n\nThis project uses [`poetry`](https://python-poetry.org). Install it using the following command.\n```bash\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -\n```\nMore instructions [here](https://python-poetry.org/docs/#installation)\n\n### Install the dependencies:\n\n`poetry install`\n\nInstall pre-commit hooks:\n\n`poetry run pre-commit install`\n\n### Running Tests:\n\n`poetry run pyscript tests`\n',
    'author': 'Anthony Almarza',
    'author_email': 'anthony.almarza@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
