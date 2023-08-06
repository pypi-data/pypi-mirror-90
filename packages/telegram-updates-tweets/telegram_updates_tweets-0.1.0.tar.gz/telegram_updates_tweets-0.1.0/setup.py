# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegram_updates_tweets']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'pymongo>=3.11.2,<4.0.0',
 'telethon>=1.18.2,<2.0.0',
 'tweepy>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'telegram-updates-tweets',
    'version': '0.1.0',
    'description': 'This package monitors the number of participants in a telegram channel and can post gains/losses updates to twitter',
    'long_description': None,
    'author': 'Alexander Jahn',
    'author_email': 'jahn.alexander@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
