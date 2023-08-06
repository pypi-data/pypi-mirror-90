# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asure',
 'asure.exceptions',
 'asure.models',
 'asure.models.routes',
 'asure.models.websocket',
 'asure.primitive',
 'asure.request',
 'asure.resource',
 'asure.template']

package_data = \
{'': ['*']}

install_requires = \
['uvicorn==0.12.2']

setup_kwargs = {
    'name': 'asure',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'JorgeFernando',
    'author_email': 'jorgebg2016@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
