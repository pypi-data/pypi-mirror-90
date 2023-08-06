# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dtb', 'dtb.mapped_collection']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dtb.mapped-collection',
    'version': '3.1.0',
    'description': '',
    'long_description': None,
    'author': 'Dima Doroshev',
    'author_email': 'dima@doroshev.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
