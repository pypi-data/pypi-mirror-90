# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aerie', 'aerie.drivers']

package_data = \
{'': ['*']}

install_requires = \
['PyPika>=0.44.0,<0.45.0']

extras_require = \
{'full': ['aiosqlite>=0.16.0,<0.17.0', 'asyncpg>=0.21.0,<0.22.0'],
 'pgsql': ['asyncpg>=0.21.0,<0.22.0'],
 'sqlite': ['aiosqlite>=0.16.0,<0.17.0']}

setup_kwargs = {
    'name': 'aerie',
    'version': '0.1.0',
    'description': 'A database toolkit.',
    'long_description': None,
    'author': 'alex.oleshkevich',
    'author_email': 'alex.oleshkevich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
