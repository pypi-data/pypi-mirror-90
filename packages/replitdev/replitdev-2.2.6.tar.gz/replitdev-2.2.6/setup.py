# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['replitdev', 'replitdev.audio', 'replitdev.database', 'replitdev.web']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'flask>=1.1.2,<2.0.0',
 'requests-html>=0.10.0,<0.11.0',
 'typing_extensions>=3.7.4,<4.0.0',
 'werkzeug>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'replitdev',
    'version': '2.2.6',
    'description': 'A library for interacting with features of repl.it',
    'long_description': '# `replit` Python Module\n\n\nThe [Repl.it](https://repl.it/) Python environment does not require any platform-specific code, however, these optional utilities provide additional platform features in a simple and accessible way.\n\n![compute](https://github.com/kennethreitz42/replit-py/blob/kr-cleanup/ext/readme.gif?raw=true)\n\n\n*Example*: [Repl.it DB](https://docs.repl.it/misc/database) is an HTTP service, but an optional Python client (here!) is available.\n\n\n### `>>> import replit`\n\nThis repository is the home for the `replit` Python package, which provides:\n\n- A fully-featured database client for [Repl.it DB](https://docs.repl.it/misc/database). **[[docs]](https://example.com)**\n- A **work in progress** Repl.it user profile lookup. **[[docs]](https://example.com)**\n- A Flask application decorator for ensuring Repl.it Auth required on specific routes. **[[docs]](https://example.com)**\n\n& other helpful toys and utilities, like...\n\n- A simple audio library that can play tones and audio files!\n- Some helpful functions for displaying ANSI colors within interactive terminal sessions.\n\n### Open Source License\n\nThis library is licensed under the [ISC License](https://en.wikipedia.org/wiki/ISC_license) and is free for you to use, change, or even profit from!\n',
    'author': 'mat',
    'author_email': 'pypi@matdoes.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/replit/replit-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
