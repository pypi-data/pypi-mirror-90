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
    'version': '2.0.1',
    'description': 'Simple fish-text.ru python wrapper',
    'long_description': '<h1 align="center">Fish-text.ru python wrapper</h1>\n\nЭта небольшая обёртка позволяет использовать API с сайта Fish-text.ru для генерации так называемого "текста-рыбы" или "рыботекста"\n\nТестировано на Python 3.8, 3.9.1\n\n## Примеры использования\n* В вашем проекте необходимо заполнить базу данных каким-то текстовым контентом\n* Собственно, наверное, это все ¯\\_(ツ)_/¯\n\n## Установка\nУстановить стабильную версию с PyPi:\n```\npython -m pip install fish_text_ru \n```\nУстановить с GitHub:\n```\npython -m pip install git+https://github.com/kiriharu/fish_text_ru\n```\n\n## Использование\n### Json Wrapper (рекомендуется)\n\n```python\n# Импортируем FishTextJson и TextType, нужный нам.\n# В методе .get() вернется по итогу объект JsonAPIResponse\nfrom fishtext import FishTextJson\nfrom fishtext.types import TextType, JsonAPIResponse\n\n# Делаем объект\napi = FishTextJson(text_type=TextType.Title)\n# Используем!\ntitles = api.get(1)\n\n# Используем JsonAPIResponse\nprint(titles.status)\nprint(titles.errorCode)\nprint(titles.text)\n```\n\n### Html wrapper\n```python\n\nfrom fishtext import FishTextHtml\nfrom fishtext.types import TextType\n\n# Делаем объект\napi = FishTextHtml(text_type=TextType.Title)\n# Используем!\ntitle = api.get(1)\n\nprint(title) # <p> какой-то там title </p>\n\n```',
    'author': 'kiriharu',
    'author_email': 'kiriharu@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kiriharu/fish_text_ru',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
