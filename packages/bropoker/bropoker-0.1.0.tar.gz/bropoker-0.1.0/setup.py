# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bropoker']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bropoker',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': '7brothers',
    'author_email': '7brothers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
