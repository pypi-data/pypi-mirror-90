# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trio_future']

package_data = \
{'': ['*']}

install_requires = \
['trio>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'trio-future',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Dan Frank',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
