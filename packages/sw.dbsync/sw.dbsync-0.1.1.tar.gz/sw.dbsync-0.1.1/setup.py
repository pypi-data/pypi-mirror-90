# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbsync']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sw.dbsync',
    'version': '0.1.1',
    'description': 'Implementation of a database synchronization schema for PEP 249 compliant databases.',
    'long_description': '',
    'author': 'Simon Wrede',
    'author_email': 'simwr872@student.liu.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
