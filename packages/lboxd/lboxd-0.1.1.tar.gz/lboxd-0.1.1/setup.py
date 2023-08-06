# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lboxd']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'rich>=9.6.1,<10.0.0']

setup_kwargs = {
    'name': 'lboxd',
    'version': '0.1.1',
    'description': 'Letterboxd user tools.',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
