# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyebus']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0']

setup_kwargs = {
    'name': 'pyebus',
    'version': '0.1.0',
    'description': 'Pythonic Interface to EBUS Daemon (ebusd)',
    'long_description': None,
    'author': 'c0fec0de',
    'author_email': 'c0fec0de@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
