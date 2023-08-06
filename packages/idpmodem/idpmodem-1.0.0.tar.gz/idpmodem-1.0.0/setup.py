# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idpmodem', 'idpmodem.codecs']

package_data = \
{'': ['*']}

install_requires = \
['aioserial>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'idpmodem',
    'version': '1.0.0',
    'description': 'A library for interfacing with an Inmarsat IsatData Pro satellite modem using serial AT commands.',
    'long_description': None,
    'author': 'G.Bruce-Payne',
    'author_email': 'geoff.bruce-payne@inmarsat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
