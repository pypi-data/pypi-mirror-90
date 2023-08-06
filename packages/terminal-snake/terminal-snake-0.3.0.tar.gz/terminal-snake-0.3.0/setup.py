# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terminal_snake']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'terminal-snake',
    'version': '0.3.0',
    'description': '',
    'long_description': '# Terminal Snake\nThis is a simple snake game to play inside a shell, written in Python.\nAfter installing (`pip install terminal_snake`) run the game with the command\n`python -m terminal_snake`. To create your own frontend you can import the\nclass `Game` from this module.',
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
