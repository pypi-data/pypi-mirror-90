# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linkace_cli', 'linkace_cli.api', 'linkace_cli.cli', 'linkace_cli.models']

package_data = \
{'': ['*'], 'linkace_cli.cli': ['templates/*']}

install_requires = \
['marshmallow>=3.10.0,<4.0.0',
 'pylint>=2.6.0,<3.0.0',
 'requests>=2.25.0,<3.0.0',
 'rich>=9.5.1,<10.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['linkace = linkace_cli:main']}

setup_kwargs = {
    'name': 'linkace-cli',
    'version': '1.0.0',
    'description': 'A CLI for the LinkAce API',
    'long_description': '# linkace-cli\nA CLI for the API of LinkAce (https://github.com/Kovah/LinkAce)\n',
    'author': 'Evan Smith',
    'author_email': 'me@iamevan.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
