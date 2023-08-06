# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aio_goodreads', 'aio_goodreads.types', 'aio_goodreads.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'aio-goodreads',
    'version': '0.1.1',
    'description': 'Asyncronous Python wrapper for Goodreads API',
    'long_description': None,
    'author': 'Mykola Solodukha',
    'author_email': 'mykola.soloduha@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
