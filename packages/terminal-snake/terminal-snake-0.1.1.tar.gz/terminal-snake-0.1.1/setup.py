# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terminal-snake']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'terminal-snake',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Terminal Snake\nThis is a simple snake game to play inside a shell, written in Python.\nSimply run the `__init__.py` file inside the `terminal-snake` directory.\nThis project requires minimum Python 3.8. To create your own frontend you\ncan import the class `Game` from `game.py`.',
    'author': 'Julian Leucker',
    'author_email': 'leuckerj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ZugBahnHof/terminal-snake',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
