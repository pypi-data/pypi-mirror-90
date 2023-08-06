# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegram_updates_tweets']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'telethon>=1.18.2,<2.0.0', 'tweepy>=3.10.0,<4.0.0']

extras_require = \
{'logging': ['pymongo>=3.11.2,<4.0.0', 'matplotlib>=3.3.3,<4.0.0'],
 'monitoring': ['Flask>=1.1.2,<2.0.0', 'waitress>=1.4.4,<2.0.0']}

setup_kwargs = {
    'name': 'telegram-updates-tweets',
    'version': '0.1.4',
    'description': 'This package monitors the number of participants in a telegram channel and can post gains/losses updates to twitter',
    'long_description': "# Telegram Updates Tweets\nThis package monitors the number of participants in a telegram channel and can post gains/losses updates to twitter.\nIt requires a twitter API key and telegram API key.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install telegram_updates_tweets.\n\n### Simple version\n\n```bash\npip install telegram_updates_tweets\n```\n\n### With monitoring and database logging\n\n```bash\npip install telegram_updates_tweets[logging,monitoring]\n```\n\n## Usage\nThe package is configured with a bunch of options.\n\n```cmd\npython -m telegram_updates_tweets --tweet-losses 100 --twitter-key OopN17481741985zgmRg0FVAOzC --twitter-secret VWyvs87I091508915HWAJDdb4XlwOLPkQXOTPbcETEV8HlvmnCx --twitter-access-token 1341085719874981434437-1zh50lhr3WEJhjfabfhdK8oYGrSh3eW --twitter-access-token-secret 5jGpCn79Z8714871kjlafjagaXr7VKeNEKWQVzzU --telegram-api-id 2015515 --telegram-api-hash b7dae63689015901efeffc69 --mongodb 127.0.0.1:27017 --telegram-channel-name CHANNELNAME --tweet-loss-template 'Der Telegram Kanal hat {loss_step} Leser verloren und ist jetzt bei {count}' --tweet-graph-template '24h Bericht, aktuelle Anzahl der Leser ist {count}, Änderung {total_change:+d} Leser' --tweet-graph 20 --tweet-graph-img-template 'Innerhalb der letzten {hours} Std.: {total_change:+d} Leser'\n```\n\n## Options\n```text\nUsage: python -m telegram_updates_tweets [OPTIONS]\n\n  Connects to telegram as a user and checks every 60minutes the subscriber\n  count of the given channel. It allows to tweet gains and/or losses with\n  additional info.\n\nOptions:\n  --tweet-gains INTEGER           Deactivated if <=0, otherwise describes the\n                                  step. Example: 100 -> tweet at 1900, 2000,\n                                  2100, ...\n\n  --tweet-losses INTEGER          Deactivated if <=0, otherwise describes the\n                                  step. Example: 100 -> tweet at 2100, 2000,\n                                  1900, ...\n\n  --tweet-loss-template TEXT      This template will be formatted and posted\n                                  on loss\n\n  --tweet-gain-template TEXT      This template will be formatted and posted\n                                  on gain\n\n  --tweet-graph INTEGER           Deactivated if <0, otherwise 0..23 specifies\n                                  the time when to post a 24h summary graph\n                                  (requires mongodb)\n\n  --tweet-graph-template TEXT     This template will be formatted and posted\n                                  if --tweet-graph is specified\n\n  --tweet-graph-img-template TEXT\n                                  This template will be formatted and used in\n                                  the image if --tweet-graph is specified\n\n  --monitoring-port INTEGER       Deactivated if <=0, otherwise 0..65000\n                                  specifies the port which allows to fetch\n                                  monitoring information. Requires\n                                  --monitoring-password\n\n  --monitoring-password TEXT      Is required if --monitoring-port is set. Is\n                                  used in basic authentication password,\n                                  username can be any.\n\n  --check-frequency INTEGER       Check period in seconds\n  --twitter-key TEXT              Also called API key, is created by the\n                                  twitter app\n\n  --twitter-secret TEXT           The secret of the twitter app\n  --twitter-access-token TEXT     The access token of the oauth procedure\n  --twitter-access-token-secret TEXT\n                                  The secret of the oauth access token\n  --telegram-api-id INTEGER       The number created by telegram\n  --telegram-api-hash TEXT        The api hash created by telegram\n  --telegram-channel-name TEXT    The name of the channel of interest\n  --mongodb TEXT                  IP:PORT of the mongo db, if not set, no data\n                                  will be logged\n\n  --help                          Show this message and exit.\n```\n\n## Development\n1. After cloning this repo execute `git config core.hooksPath hooks` in the root directory.\n2. Install poetry https://python-poetry.org/docs/\n3. `poetry config settings.virtualenvs.in-project true`\n4. `poetry install`\n4. `poetry shell`\n\n## API keys\nTo use this package a twitter API key and a telegram API key are needed, these keys will be used to request OAUTH tokens from one twitter account and a telegram account.\n\n1. Create a twitter APP with 'write' permission https://developer.twitter.com/en/portal/projects-and-apps\n- this creates the `--twitter-key` and the ` --twitter-secret`\n- the application will print a `authorization link`, open it, give permission to your own app the use your twitter profile\n- it will print the `--twitter-access-token` and `--twitter-access-token-secret`\n- all subsequent calls should use all four parameters\n2. Create a telegram APP as described in https://core.telegram.org/api/obtaining_api_id\n- this generates a `--telegram-api-id` (numbers) and `--telegram-api-hash` (string)\n- when the appication is started with this parameters, it will ask for your phone number, you will receive a code from telegram, enter it in the application\n- this will create a token file called 'anon.session' and 'anon.session-jornal'\n- all subsequent calls should not prompt for other info\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n",
    'author': 'Alexander Jahn',
    'author_email': 'jahn.alexander@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AlxndrJhn/telegram_updates_tweets',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
