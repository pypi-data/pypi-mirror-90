# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['newscraping',
 'newscraping.application',
 'newscraping.infrastructure',
 'newscraping.settings']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'pandas>=1.2.0,<2.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['newscraping = newscraping.application.scraping:news']}

setup_kwargs = {
    'name': 'newscraping',
    'version': '0.1.2',
    'description': 'Web scraping of financial headlines',
    'long_description': '# Newscraping\n\n[\n![PyPI](https://img.shields.io/pypi/v/newscraping)\n![PyPI](https://img.shields.io/pypi/l/newscraping)\n](https://pypi.org/project/newscraping/)\n\nThis package makes webscraping of financial headlines easy. \n\n## Suported sources:\n\n- reuters.com/finance/markets\n- ft.com/markets\n\n## Installation\n\nNewscraping can be installed from PyPI using `pip` or your package manager of choice:\n\n```\npip install newscraping\n```\n\n## Usage\n\n### CLI\n\nYou can use newscraping as a CLI tool using the `newscraping` command.  \nThe package will get the latest headline from reuters and print is in the terminal.  \nThis is mainly for testing purposes. \n\n### Python script\n\nYou can import the newscraping package in your python project using:\n\n```\nfrom newscraping import news\n```\n\nAnd then use it as:\n\n```\ndf = news(newspaper="reuters", n_articles=-1, early_date="2020-01-01", verbose=0)\n```\n\n- With the default parameters (see above), only the last headline from reuters will be returned\n- newspaper argument must be in ["reuters", "financial times"]\n- n_articles argument is the number of articles to return, starting with the most recent ones\n- early_date argument is the publication date of the earliest article to return\n- If both n_articles and early_date are provided, the script will stop scraping when the any condition is met\n- Pass verbose=1 to print in the progress of websraping (current page and publication date)\n\n### List of available sources\n\nYou can get the list of available sources this package is configured for calling:\n\n```\nfrom newscraping import newspapers\navailable_sources = newspapers()\n```\n',
    'author': 'Jerome Blin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/financial-sentiment/newscraping',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
