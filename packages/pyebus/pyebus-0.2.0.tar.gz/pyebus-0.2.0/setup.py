# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyebus', 'pyebus.cli']

package_data = \
{'': ['*']}

install_requires = \
['anytree>=2.8.0,<3.0.0']

entry_points = \
{'console_scripts': ['ebt = pyebus.cli:main']}

setup_kwargs = {
    'name': 'pyebus',
    'version': '0.2.0',
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
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
