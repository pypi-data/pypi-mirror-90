# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dispike',
 'dispike.errors',
 'dispike.helper',
 'dispike.middlewares',
 'dispike.models',
 'dispike.models.discord_types',
 'dispike.register',
 'dispike.register.models']

package_data = \
{'': ['*']}

install_requires = \
['PyNaCl>=1.4.0,<2.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'httpx>=0.16.1,<0.17.0',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.7.3,<2.0.0',
 'typing-extensions>=3.7.4,<4.0.0',
 'uvicorn>=0.13.2,<0.14.0']

setup_kwargs = {
    'name': 'dispike',
    'version': '0.5.5a0',
    'description': 'library for interacting with discord slash commands via an independently hosted server. Powered by FastAPI',
    'long_description': '# dispike\n\n***\n[![codecov](https://codecov.io/gh/ms7m/dispike/branch/master/graph/badge.svg?token=E5AXLZDP9O)](https://codecov.io/gh/ms7m/dispike) ![Test Dispike](https://github.com/ms7m/dispike/workflows/Test%20Dispike/badge.svg?branch=master) ![PyPi Link](https://img.shields.io/badge/Available%20on%20PyPi-Dispike-blue?logo=pypi&link=%22https://pypi.org/project/dispike%22) ![PyPiVersion](https://img.shields.io/badge/dynamic/json?color=blue&label=PyPi%20Version&query=%24.info.version&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fdispike%2Fjson)\n\n***\n\n\n\nan *extremely-extremely* early WIP library for easily creating REST-based webhook bots for discord using the new Slash Commands feature. \n\nPowered by FastAPI.\n\n\n\n## Example (a simple bot)\n\n```python\n\n# Incoming models use this.\nfrom dispike.models.incoming import IncomingDiscordInteraction # For Type Hinting\n\n# Main Dispike Object\nfrom dispike import Dispike\n\n# For creating commands.\nfrom dispike.register.models import DiscordCommand, CommandOption, CommandChoice, CommandTypes\n\n# For responding to commands.\nfrom dispike.response import DiscordResponse\n\n\nbot = Dispike(\n  client_public_key="< PublicKey >"\n  bot_token="< Bot Token >",\n  application_id="< AppID >"\n)\n\n\n\n# Let\'s register a command.\n# /wave <person>\n# Learn more about registering commands in the Discord Docs.\n\ncommand_to_be_created = DiscordCommand(\n    name="wave" # this is the main command name.,\n    description="Send a wave to a nice person! 👋 ",\n    options=[\n        CommandOption(\n            name="person" # this is the attribute assigned to the value passed.,\n            description="person to target" # this describes the value to pass,\n          \trequired=True,\n            type=CommandTypes.USER\n        )\n    ]\n)\n\n# Nice, we created a command. /wave <person to ping>. Let\'s register it.\n\nbot.register(\n\tcommand_to_be_created\n)\n\n\n# We\'ve registered, now it\'s time to build the bot! \n# Arguments that you pass to your function are \n# the same arguments you defined/registered with discord..\n# Don\'t forget to have an argument for a ctx (context). \n\n@bot.interaction.on("wave")\nasync def handle_send_wave(person: int, ctx: IncomingDiscordInteraction):\n  logger.info("Recieved a wave!")\n  \n\n  # this is what we will be returning. Let\'s edit it.\n  # Discord will pass the user id..\n  _response = DiscordResponse()\n  _response.content f"👋 Hi @<{person}>."\n  \n  return _response.response\n  \n# Run your bot.\n# Powered by uvicorn.\n\nbot.run(port=5000)\n    \n```\nEmbeds are also available (Copied from Discord.py)\n\n```python\nfrom dispike.helper import Embed\n\n_response = DiscordResponse()\n_response.embed = Embed() # your embed created.\n```\n\n## Getting, Deleting and Editing Commands\n\n\n\n```python\nfrom dispike import Dispike\n\n# For creating commands.\nfrom dispike.register.models import DiscordCommand, CommandOption, CommandChoice, CommandTypes\n\n\nbot = Dispike(\n\tclient_public_key="< PublicKey >"\n  bot_token="< Bot Token >",\n  application_id="< AppID >"\n)\n\nall_commands = bot.get_commands()\n\nfor command in all_commands:\n  print(f"{command.name} -> {command.id}")\n \ntarget_command = all_commands[0]\n\ncommand_to_be_created = DiscordCommand(\n    name="salute" # this is the main command name.,\n    description="Send a salute to a nice person! ",\n    options=[\n        CommandOption(\n            name="person" # this is the attribute assigned to the value passed.,\n            description="person to target" # this describes the value to pass,\n          \trequired=True,\n            type=CommandTypes.USER\n        )\n    ]\n)\n\nbot.edit_command(target_command.id, command_to_be_created)\nbot.delete_command(all_commands[1].id)\n```\n\n\n\nWhen configuring your endpoint on discord settings, be sure to append ``/interactions`` to your domain.\n\n<p >\n    <img\n      alt="Website"\n      src="./docs/images/domain.png"\n    />\n</p>\n\n## Caveats\n\n- ~~Does not handle registring new commands.~~\n- ~~Does not handle anything other then string responses. (However you are free to return any valid dict in your handler.)~~\n- ~~Not on PyPi~~\n- Does not speak over the discord gateway. You\'ll need a server to handle requests and responses.\n- Python 3.6+\n- Does not support the following endpoints\n  - [Create Followup Message](https://discord.com/developers/docs/interactions/slash-commands#create-followup-message)\n  - [Edit Followup Message](https://discord.com/developers/docs/interactions/slash-commands#edit-followup-message)\n  - [Delete Followup Message](https://discord.com/developers/docs/interactions/slash-commands#delete-followup-message)\n- Handling followup messages.\n\n\n\n# Development\n\nHelp is wanted in mantaining this library. Please try to direct PRs to the ``dev`` branch, and use black formatting (if possible).\n\n![Test Dispike](https://github.com/ms7m/dispike/workflows/Test%20Dispike/badge.svg?branch=dev)\n',
    'author': 'Mustafa Mohamed',
    'author_email': 'ms7mohamed@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ms7m/dispike',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
