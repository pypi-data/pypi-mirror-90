# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lboxd']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'requests>=2.0.0,<3.0.0', 'rich>=9.6.1,<10.0.0']

entry_points = \
{'console_scripts': ['lboxd = lboxd:main']}

setup_kwargs = {
    'name': 'lboxd',
    'version': '0.1.6',
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
    'entry_points': entry_points,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
