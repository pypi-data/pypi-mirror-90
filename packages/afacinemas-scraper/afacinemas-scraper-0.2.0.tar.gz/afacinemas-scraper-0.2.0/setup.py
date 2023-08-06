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
    'version': '0.2.0',
    'description': 'Ferramenta para raspagem de dados do site da rede Afa Cinemas',
    'long_description': '# Afa Cinemas Scraper 🦀\nFerramenta para raspagem de dados do site da rede [Afa Cinemas](http://afacinemas.com.br/).\n\n## Instalação\n\n```sh\npip install afacinemas-scraper\n```\n\n## Uso \n\n```python\nfrom afacinemas_scraper import Scraper\n\nscraper = Scraper()\ncinemas = scraper.get_cinemas()\n\nprint(cinemas)\n```\n',
    'author': 'Douglas Gusson',
    'author_email': 'douglasgusson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/douglasgusson/afacinemas-scraper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
