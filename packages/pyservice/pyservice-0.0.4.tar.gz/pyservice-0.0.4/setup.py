# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyservice']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyservice',
    'version': '0.0.4',
    'description': 'A light-service like project in Python',
    'long_description': None,
    'author': 'Attila Domokos',
    'author_email': 'adomokos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
