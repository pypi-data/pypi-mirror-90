# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['afacinemas_scraper', 'afacinemas_scraper.core']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'requests-cache>=0.5.2,<0.6.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'afacinemas-scraper',
    'version': '0.3.0',
    'description': 'Ferramenta para raspagem de dados do site da rede Afa Cinemas',
    'long_description': "# Afa Cinemas Scraper 🦀\n\n> **afacinemas-scraper** - Ferramenta para raspagem de dados do site da rede [Afa Cinemas](http://afacinemas.com.br/).\n\n[![GitHub license](https://img.shields.io/github/license/douglasgusson/afacinemas-scraper)](https://github.com/douglasgusson/afacinemas-scraper/blob/main/LICENSE)\n[![GitHub issues](https://img.shields.io/github/issues/douglasgusson/afacinemas-scraper)](https://github.com/douglasgusson/afacinemas-scraper/issues)\n[![GitHub forks](https://img.shields.io/github/forks/douglasgusson/afacinemas-scraper)](https://github.com/douglasgusson/afacinemas-scraper/network)\n[![GitHub stars](https://img.shields.io/github/stars/douglasgusson/afacinemas-scraper)](https://github.com/douglasgusson/afacinemas-scraper/stargazers)\n\n## ⚙️ Instalação\n\n```sh\npip install afacinemas-scraper\n```\n\n## 💻 Utilização \n\n```python\nfrom afacinemas_scraper import Scraper\n\nscraper = Scraper()\n```\n\n### 🔍 Buscando os cinemas \n\n```python\nfrom afacinemas_scraper import Scraper\n\nscraper = Scraper()\ncinemas = scraper.get_cinemas()\n\nprint(cinemas)\n```\n\n📄 Saída:\n```python\n[{'codigo': 4, 'nome': 'Boituva Cine Park', 'logo': 'http://afacinemas.com.br/logotipo/boituva.jpg', 'endereco': 'Avenida Vereador José Biagione, 660 Centro - Boituva /SP', 'contato': '(15) 3363-8083'}, ...]\n```\n\n### 🔍 Buscando os próximos lançamentos\n\n```python\nfrom afacinemas_scraper import Scraper\n\nscraper = Scraper()\n\nproximos_lancamentos = scraper.get_proximos_lancamentos()\nprint(proximos_lancamentos)\n```\n\n📄 Saída:\n```python\n[{'titulo': 'MONSTER HUNTER', 'estreia': '14/01/2021', 'poster': 'http://afacinemas.com.br/adm/cartazSite/hunter.jpg', 'descricao': 'Baseado no jogo da Capcom chamado Monster Hunter, a tenente Artemis e seus soldados são transportados para um novo mundo. Lá, eles se envolvem em batalhas imponentes, buscando desesperadamente a sobrevivência contra bestas gigantes portadoras de habilidades surreais.', 'classificacao': '14 ANOS', 'genero': 'AÇÃO', 'duracao': '110min'}, ...]\n```\n\n### 🔍 Buscando os preços dos ingressos\n\n```python\nfrom afacinemas_scraper import Scraper\n\nscraper = Scraper()\n\nprecos_ingressos = afa.get_precos_ingressos(10)  # código do cinema\nprint(precos_ingressos)\n```\n\n📄 Saída:\n```python\n[{'dia_semana': 'Domingo', 'precos': [{'descricao': 'Inteira 2D', 'valor': 24.0}, {'descricao': 'Meia 2D', 'valor': 12.0}, {'descricao': 'Inteira 3D', 'valor': 24.0}, {'descricao': 'Meia 3D', 'valor': 12.0}]}, ...]\n```\n",
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
