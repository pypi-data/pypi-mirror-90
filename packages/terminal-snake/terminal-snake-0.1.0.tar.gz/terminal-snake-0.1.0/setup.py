# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terminal-snake']

package_data = \
{'': ['*'],
 'terminal-snake': ['.git/*',
                    '.git/hooks/*',
                    '.git/info/*',
                    '.git/logs/*',
                    '.git/logs/refs/heads/*',
                    '.git/logs/refs/remotes/origin/*',
                    '.git/objects/0a/*',
                    '.git/objects/16/*',
                    '.git/objects/22/*',
                    '.git/objects/29/*',
                    '.git/objects/35/*',
                    '.git/objects/3e/*',
                    '.git/objects/3f/*',
                    '.git/objects/40/*',
                    '.git/objects/41/*',
                    '.git/objects/46/*',
                    '.git/objects/47/*',
                    '.git/objects/64/*',
                    '.git/objects/68/*',
                    '.git/objects/78/*',
                    '.git/objects/8c/*',
                    '.git/objects/9f/*',
                    '.git/objects/a7/*',
                    '.git/objects/ad/*',
                    '.git/objects/b1/*',
                    '.git/objects/ba/*',
                    '.git/objects/c0/*',
                    '.git/objects/c5/*',
                    '.git/objects/e6/*',
                    '.git/objects/ef/*',
                    '.git/objects/fd/*',
                    '.git/refs/heads/*',
                    '.git/refs/remotes/origin/*',
                    'dist/*']}

setup_kwargs = {
    'name': 'terminal-snake',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Julian Leucker',
    'author_email': 'leuckerj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
