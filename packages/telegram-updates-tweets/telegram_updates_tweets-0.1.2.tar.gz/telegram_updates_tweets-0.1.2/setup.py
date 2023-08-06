# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegram_updates_tweets']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'pymongo>=3.11.2,<4.0.0',
 'telethon>=1.18.2,<2.0.0',
 'tweepy>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'telegram-updates-tweets',
    'version': '0.1.2',
    'description': 'This package monitors the number of participants in a telegram channel and can post gains/losses updates to twitter',
    'long_description': "# Telegram Updates Tweets\nThis package monitors the number of participants in a telegram channel and can post gains/losses updates to twitter.\nIt requires a twitter API key and telegram API key.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install telegram_updates_tweets.\n\n```bash\npip install telegram_updates_tweets\n```\n\n## Usage\nThe package is configured with a bunch of options.\n```cmd\npython -m telegram_updates_tweets --tweet-losses 100 --twitter-key OopN17481741985zgmRg0FVAOzC --twitter-secret VWyvs87I091508915HWAJDdb4XlwOLPkQXOTPbcETEV8HlvmnCx --twitter-access-token 1341085719874981434437-1zh50lhr3WEJhjfabfhdK8oYGrSh3eW --twitter-access-token-secret 5jGpCn79Z8714871kjlafjagaXr7VKeNEKWQVzzU --telegram-api-id 2015515 --telegram-api-hash b7dae63689015901efeffc69 --mongodb 127.0.0.1:27017 --telegram-channel-name CHANNELNAME --tweet-loss-template 'Der Telegram Kanal hat {loss_step} Leser verloren und ist jetzt bei {count}' --tweet-graph-template '24h Bericht, aktuelle Anzahl der Leser ist {count}, Änderung {total_change:+d} Leser' --tweet-graph 20 --tweet-graph-img-template 'Innerhalb der letzten {hours} Std.: {total_change:+d} Leser'\n```\n\n## Options\n```text\nUsage: python -m telegram_updates_tweets [OPTIONS]\n\n  Connects to telegram as a user and checks every 60minutes the subscriber\n  count of the given channel. It allows to tweet gains and/or losses with\n  additional info. It has a small web interface to configure access to\n  social media.\n\nOptions:\n  --tweet-gains INTEGER           Deactivated if <=0, otherwise describes the\n                                  step. Example: 100 -> tweet at 1900, 2000,\n                                  2100, ...\n\n  --tweet-losses INTEGER          Deactivated if <=0, otherwise describes the\n                                  step. Example: 100 -> tweet at 2100, 2000,\n                                  1900, ...\n\n  --tweet-loss-template TEXT      This template will be formatted and posted\n                                  on loss\n\n  --tweet-gain-template TEXT      This template will be formatted and posted\n                                  on gain\n\n  --tweet-graph INTEGER           Deactivated if <0, otherwise 0..23 specifies\n                                  the time when to post a 24h summary graph\n                                  (requires mongodb)\n\n  --tweet-graph-template TEXT     This template will be formatted and posted\n                                  if --tweet-graph is specified\n\n  --tweet-graph-img-template TEXT\n                                  This template will be formatted and used in\n                                  the image if --tweet-graph is specified\n\n  --twitter-key TEXT              Also called API key, is created by the\n                                  twitter app\n\n  --twitter-secret TEXT           The secret of the twitter app\n  --twitter-access-token TEXT     The access token of the oauth procedure\n  --twitter-access-token-secret TEXT\n                                  The secret of the oauth access token\n  --telegram-api-id INTEGER       The number created by telegram\n  --telegram-api-hash TEXT        The api hash created by telegram\n  --telegram-channel-name TEXT    The name of the channel of interest\n  --mongodb TEXT                  IP:PORT of the mongo db, if not set, no data\n                                  will be logged\n\n  --help                          Show this message and exit.\n```\n\n## Development\n1. After cloning this repo execute `git config core.hooksPath hooks` in the root directory.\n2. Install poetry https://python-poetry.org/docs/\n3. `poetry config settings.virtualenvs.in-project true`\n4. `poetry install`\n4. `poetry shell`\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n",
    'author': 'Alexander Jahn',
    'author_email': 'jahn.alexander@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AlxndrJhn/telegram_updates_tweets',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
