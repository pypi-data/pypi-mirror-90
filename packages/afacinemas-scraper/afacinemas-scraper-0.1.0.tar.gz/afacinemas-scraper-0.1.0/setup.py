# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['afacinemas_scraper']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'requests-cache>=0.5.2,<0.6.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'afacinemas-scraper',
    'version': '0.1.0',
    'description': 'Ferramenta para raspagem de dados do site da rede Afa Cinemas',
    'long_description': None,
    'author': 'Douglas Gusson',
    'author_email': 'douglasgusson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
