# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commanderbot_ext',
 'commanderbot_ext.faq',
 'commanderbot_ext.status',
 'commanderbot_ext.vote']

package_data = \
{'': ['*']}

install_requires = \
['commanderbot-lib>=0.5.0,<0.6.0', 'discord.py>=1.5.0,<2.0.0']

setup_kwargs = {
    'name': 'commanderbot-ext',
    'version': '0.5.0',
    'description': 'A collection of cogs and extensions for discord.py bots.',
    'long_description': '# CommanderBot Ext\n\nA collection of cogs and extensions for discord.py bots.\n\n[![package-badge]](https://pypi.python.org/pypi/commanderbot-ext/)\n[![version-badge]](https://pypi.python.org/pypi/commanderbot-ext/)\n\n[package-badge]: https://img.shields.io/pypi/v/commanderbot-ext.svg\n[version-badge]: https://img.shields.io/pypi/pyversions/commanderbot-ext.svg\n',
    'author': 'Arcensoth',
    'author_email': 'arcensoth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CommanderBot-Dev/commanderbot-ext',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
