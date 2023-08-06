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
 'bs4>=0.0.1,<0.0.2',
 'colorama>=0.4.4,<0.5.0',
 'coloredlogs>=15.0,<16.0',
 'pyfiglet>=0.8.post1,<0.9']

setup_kwargs = {
    'name': 'coin-clicker',
    'version': '1.0.6',
    'description': 'Auto-clicks telegram crypto-bot websites to earn money.',
    'long_description': '# Coin clicker\n\n![Made with love in Brazil](https://madewithlove.now.sh/br?heart=true&template=for-the-badge)\n[![Python](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)\n\n## Screenshot \n\n![CLI Screenshot](https://github.com/lee-hodg/coin-clicker/blob/master/coin_clicker.png?raw=true)\n\nThe purpose of this app is to visit telegram clickbot channels and automatically visit\nthe websites they provide in order to earn crypto-currency, such as LTC.\n\n## Requirements\n\nPython 3.6+\n\n## Installation\n\n```bash\npip install coin-clicker\n```\n\n## Running\n\n```bash\npython -m coin_clicker \n```\n\nYou will be asked to enter your phone number and then verify the code they send you on\nthe first run. Next you choose which bot you wish to visit sites for. Finally, you can choose\nwhether to run the bot in "headless" mode or not. Headless mode means you won\'t see\na browser doing the visits vs seeing Chrome popup and being automated (useful for tests).\n\nYou should see the script visiting websites provided and earning crypto for you.\nAt some point it will run out of websites to visit and wait until more become available.\n\nEnsure to run from a directory in which you have write permissions\n## Developer notes\n\nWith `poetry` there is no need to have a `setup.py` in the root. Just run\n`poetry build` and `poetry publish`. The archived in `dist/` will get a `setup.py` generated\nfrom the values in `pyproject.toml`.\n',
    'author': 'lee',
    'author_email': 'lee@logicon.io',
    'maintainer': 'lee',
    'maintainer_email': 'lee@logicon.io',
    'url': 'https://github.com/lee-hodg/coin-clicker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
