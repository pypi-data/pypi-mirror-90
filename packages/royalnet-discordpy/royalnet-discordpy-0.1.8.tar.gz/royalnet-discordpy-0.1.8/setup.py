# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['royalnet_discordpy']

package_data = \
{'': ['*']}

install_requires = \
['discord.py>=1.5.1,<2.0.0', 'royalnet>=6.0.0a31,<7.0.0']

setup_kwargs = {
    'name': 'royalnet-discordpy',
    'version': '0.1.8',
    'description': '',
    'long_description': None,
    'author': 'Stefano Pigozzi',
    'author_email': 'ste.pigozzi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
