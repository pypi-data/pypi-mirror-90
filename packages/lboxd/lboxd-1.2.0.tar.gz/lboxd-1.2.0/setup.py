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
    'version': '1.2.0',
    'description': 'Letterboxd user tools.',
    'long_description': "\n# lboxd <br> An unofficial letterboxd.com API\n\nGet reviews from letterboxd users. Done with pure HTML parsing.\n\n## Development Environment\n\n- Ubuntu 20.04 lts\n\n- Python 3.8.5\n\nThis has not been tested on Windows, there may be encoding problems.\n\n\n# Installation\n\n`pip install lboxd`\n\n# Usage\n```py\n'''\nPretty printing reviews with a generator.\n    => Generators are good for when there are requests to many different URLs.\n    => A new requests session is created for the duration of the generator.\n'''\n\nimport lboxd\nfrom bs4 import BeautifulSoup as bs\nfrom rich import print as rprint\n\nfor review in lboxd.reviews(user='redlettermedia', count=5):\n    title = review ['title']\n    review = review['review']\n    htmlPretty = bs.prettify(bs(review, 'html.parser'))\n\n    rprint(f'[yellow]Title:[/yellow] [red]{title}[/red]\\n{htmlPretty}')\n```\n\n![Redlettermedia example](https://i.imgur.com/fejIZoR.png)\n\n\n```py\nfrom lboxd import lboxdlist\nfrom rich import print as rprint\n\nfor movie in lboxdlist(user='daqoon'):\n    title = movie ['title']\n    rating = movie['rating']\n    richTitle = f'[yellow]Title:[/yellow] [red]{title}[/red]'\n\n    if rating:\n        rprint(f'{richTitle} rating={rating}')\n    else:\n        rprint(richTitle)\n```\n\n\n![Redlettermedia example](https://i.imgur.com/YXjwaN9.png)\n\n\n\n# CLI\n\n## Example\n\n![Redlettermedia example](https://i.imgur.com/34XaBY0.png)\n\n\n## Arguments\n\n  `--user USER` `-u USER`   letterboxd.com user\n\n  `--reviews` `-r`          Gets reviews\n\n  `--testing` `-t`          Testing flag - for development only\n\n  `--save-html` `-w`          Saves an HTML document for easily viewing reviews\n\n  `--browser-open` `-b`        Opens saved HTML document in the browser\n\n  `--search SEARCH [SEARCH ...]` `-s SEARCH [SEARCH ...]` Will only get search terms, currently needs to match exactly with letterboxd notation. Replace spaces with dashes.  \n",
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
