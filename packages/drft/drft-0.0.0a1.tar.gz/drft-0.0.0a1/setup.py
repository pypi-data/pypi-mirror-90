# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['drft']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0,<4.0',
 'django-filter>=2.2.0,<3.0.0',
 'djangorestframework>=3.11,<4.0']

extras_require = \
{'yasg': ['drf-yasg>=1.17,<2.0']}

entry_points = \
{'console_scripts': ['tests = tests.run:main']}

setup_kwargs = {
    'name': 'drft',
    'version': '0.0.0a1',
    'description': '',
    'long_description': "# DRFT\n\n> _Django REST Framework Toolkit (DRFT)_\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n[![codecov](https://codecov.io/gh/anthonyalmarza/drft/branch/main/graph/badge.svg?token=JRCC98L3FG)](https://codecov.io/gh/anthonyalmarza/drft)\n\n![Build](https://github.com/anthonyalmarza/drft/workflows/Build/badge.svg)\n\n## Installation\n\n`pip install drft`\n\n## Local Development\n\n### Pyenv\nIt's recommended that you use [`pyenv`](https://github.com/pyenv/pyenv)\n\n[pyenv-installer](https://github.com/pyenv/pyenv-installer)\n```bash\ncurl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash\n```\n\n### Install `poetry`\n\nThis project uses [`poetry`](https://python-poetry.org). Install it using the following command.\n```bash\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -\n```\nMore instructions [here](https://python-poetry.org/docs/#installation)\n\n### Install the dependencies:\n\n`poetry install`\n\nInstall pre-commit hooks:\n\n`poetry run pre-commit install`\n\n### Running Tests:\n\n`poetry run tests`\n",
    'author': 'Anthony Almarza',
    'author_email': 'anthony.almarza@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
