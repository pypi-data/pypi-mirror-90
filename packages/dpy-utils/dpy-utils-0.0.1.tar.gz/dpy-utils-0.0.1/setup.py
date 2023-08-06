# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0', 'python-dotenv>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'dpy-utils',
    'version': '0.0.1',
    'description': 'A discord.py utility library.',
    'long_description': '# dpy-utils\n*A [discord.py](https://github.com/rapptz/discord.py) utility library.*\n\n\n> ## Warning\n> \n> This is a very early alpha version. There might be some unknown issues.\n\n## Features\n- custom Context with additional features like `ctx.ask`\n- patched `Bot` and `AutoShardedBot` classes that that use the custom Context\n- patched `Bot` automatically loads token and prefix from `.env` file\n- `monkey_patch()` to overwrite `discord.py` classes with `dpy-utils`\n\n## Installation\n```\npip install dpy-utils\n```\n\n\n## Usage\n*.env*\n```env\nTOKEN=token\nPREFIX=?\n```\n\n*bot.py*\n```py\nimport os\n\nimport utils\nfrom discord.ext import commands\n\nutils.monkey_patch()\n\nbot: utils.Bot = commands.Bot()\n\n\n@bot.command()\nasync def test(ctx: utils.Context):\n    answer = await ctx.ask("Do you like dpy-utils?")\n    print(answer)\n\n\nbot.run()\n```\n\n\n## Requirements\n- Python >= 3.6\n- [pydantic](https://github.com/samuelcolvin/pydantic)\n- [python-dotenv](https://github.com/theskumar/python-dotenv)\n- [discord.py](https://github.com/rapptz/discord.py)\n\n## Contributing and Issues\nIf you want to contribute or want to suggest additional features please use [github issues](https://github.com/makupi/dpy-utils/issues).\n\n\n[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/A0A015HXK)\n',
    'author': 'makubob',
    'author_email': 'makupi@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/makupi/dpy-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
