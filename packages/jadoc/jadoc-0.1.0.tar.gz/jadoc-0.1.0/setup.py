# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jadoc']

package_data = \
{'': ['*']}

install_requires = \
['visedit>=1.0.4,<2.0.0', 'youcab>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'jadoc',
    'version': '0.1.0',
    'description': 'Tokenizes Japanese documents to enable CRUD operations.',
    'long_description': '# Jadoc: Tokenizes Japanese Documents to Enable CRUD Operations\n\n[![PyPI Version](https://img.shields.io/pypi/v/jadoc.svg)](https://pypi.org/pypi/jadoc/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/jadoc.svg)](https://pypi.org/pypi/jadoc/)\n[![License](https://img.shields.io/pypi/l/jadoc.svg)](https://github.com/poyo46/jadoc/blob/main/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\n## Installation\n\n**Install MeCab**\n\nMeCab is required for Jadoc to work.\nIf it is not already installed, [install MeCab](https://taku910.github.io/mecab/) first.\n\n**Install Jadoc**\n\n```console\n$ pip install jadoc\n```\n\n## Usage\nTODO\n',
    'author': 'poyo46',
    'author_email': 'poyo4rock@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/poyo46/jadoc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
