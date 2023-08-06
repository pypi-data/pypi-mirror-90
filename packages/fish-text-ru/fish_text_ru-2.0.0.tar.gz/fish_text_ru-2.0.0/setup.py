# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fishtext']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'fish-text-ru',
    'version': '2.0.0',
    'description': 'Simple fish-text.ru python wrapper',
    'long_description': None,
    'author': 'kiriharu',
    'author_email': 'kiriharu@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
