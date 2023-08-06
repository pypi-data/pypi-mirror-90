# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['chenv',
 'chenv.inputs',
 'chenv.inputs.blank',
 'chenv.inputs.heroku',
 'chenv.inputs.local',
 'chenv.models']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'httpx>=0.16.1,<0.17.0',
 'marshmallow>=3.10.0,<4.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'questionary>=1.9.0,<2.0.0',
 'toolz>=0.11.1,<0.12.0']

entry_points = \
{'console_scripts': ['chenv = chenv.main:main']}

setup_kwargs = {
    'name': 'chenv',
    'version': '0.1.0',
    'description': 'modern local environment management',
    'long_description': "[![Tests](https://github.com/jonathan-shemer/chenv/workflows/Tests/badge.svg)](https://github.com/jonathan-shemer/chenv/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/jonathan-shemer/chenv/branch/master/graph/badge.svg)](https://codecov.io/gh/jonathan-shemer/chenv)\n[![PyPI](https://img.shields.io/pypi/v/chenv.svg)](https://pypi.org/project/chenv/)\n[![Read the Docs](https://readthedocs.org/projects/chenv/badge/)](https://chenv.readthedocs.io/)\n\n```\n      _\n  ___| |__   ___ _ ____   __\n / __| '_ \\ / _ | '_ \\ \\ / /\n| (__| | | |  __| | | \\ V /\n \\___|_| |_|\\___|_| |_|\\_/ . modern local environment management\n```\n",
    'author': 'Jonathan Shemer',
    'author_email': 'i@jonathanshemer.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jonathan-shemer/chenv',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
