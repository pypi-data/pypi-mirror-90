# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybelieva']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6,<4.0', 'pydantic>=1.7,<2.0']

setup_kwargs = {
    'name': 'pybelieva',
    'version': '0.1.0.dev5',
    'description': 'Python wrapper for UnbelievaBoat API',
    'long_description': '# Pybelieva\n\n[![discord][discord-badge]][discord] [![api][api-badge]][api]\n![logo][logo]\n\nPybelieva is a library providing a Python interface\nto the [UnbelievaBoat API][api]. To\nuse it, you need to get a token from the official documentation page.\n\n## Dependencies\n\n- Python\n- aiohttp\n- discord.py (optional)\n\n## Roadmap\n\n- Documentation\n- Rate limit handling\n\n[logo]: https://i.imgur.com/RLRDeQw.png\n[discord-badge]: https://img.shields.io/discord/592830069806989339?color=4e5d94&label=Discord&logo=discord\n[discord]: https://discord.gg/jK8thg37mC\n[api]: https://unb.pizza/api/docs\n[api-badge]: https://img.shields.io/badge/api-v1-ff266a\n',
    'author': 'John Meow',
    'author_email': 'j0hn.meow@ya.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/dev-cats/Pybelieva',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
