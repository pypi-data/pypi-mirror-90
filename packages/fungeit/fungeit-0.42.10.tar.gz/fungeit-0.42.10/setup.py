# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fungeit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fungeit',
    'version': '0.42.10',
    'description': 'The edge code needed to interact with the fungeit ecosystem.',
    'long_description': None,
    'author': 'Scott McCallum',
    'author_email': 'cto@fungeit.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
