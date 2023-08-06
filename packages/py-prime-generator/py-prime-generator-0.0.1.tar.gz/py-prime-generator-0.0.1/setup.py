# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_prime_generator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-prime-generator',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Michael Tinsley',
    'author_email': 'michaeltinsley@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
