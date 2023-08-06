# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coin_clicker']

package_data = \
{'': ['*']}

install_requires = \
['PyInquirer>=1.0.3,<2.0.0',
 'Telethon>=1.18.2,<2.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'coloredlogs>=15.0,<16.0',
 'pyfiglet>=0.8.post1,<0.9',
 'selenium>=3.141.0,<4.0.0',
 'webdriver-manager>=3.2.2,<4.0.0']

setup_kwargs = {
    'name': 'coin-clicker',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'lee',
    'author_email': 'lee@logicon.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
