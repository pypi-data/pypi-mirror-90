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
    'version': '1.0.0',
    'description': 'Letterboxd user tools.',
    'long_description': '\n# letterboxd\n\n![Redlettermedia example](./geta-all-example.gif)\n\npython3 movies.py\n\nArguments\n\n  `--user USER` `-u USER`   letterboxd.com user\n\n  `--reviews` `-r`          Gets reviews\n\n  `--testing` `-t`          Testing flag - for development only\n\n  `--save-json` `-j`        Saves a JSON file of the reviews dictionary\n\n  `--save-html` `-w`          Saves an HTML document for easily viewing reviews\n\n  `--browser-open` `-b`        Opens saved HTML document in the browser\n\n  `--search SEARCH [SEARCH ...]` `-s SEARCH [SEARCH ...]`\n',
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
