# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytt']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['tt = pytt.main:main']}

setup_kwargs = {
    'name': 'pytt',
    'version': '0.1.0',
    'description': 'Python Time Tracker',
    'long_description': 'Python script for time tracking.\n\n# Installation\n\n`pip install pytt`\n\n# Usage\n\n```\nUsage: tt [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n\n  --help                          Show this message and exit.\n\nCommands:\n  in      Start clock.\n  log     Print log.\n  out     End clock.\n  stats   Show daily stats.\n  status  Show current clock.\n```\n',
    'author': 'pajecawav',
    'author_email': 'pajecawav@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pajecawav/pytt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
