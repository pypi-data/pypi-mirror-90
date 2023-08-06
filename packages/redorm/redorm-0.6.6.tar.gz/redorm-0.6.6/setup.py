# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redorm']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-jsonschema[fast-validation]>=2.13.0,<3.0.0',
 'environs>=9.3.0,<10.0.0',
 'fakeredis>=1.4.5,<2.0.0',
 'redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'redorm',
    'version': '0.6.6',
    'description': 'A simple redis ORM',
    'long_description': None,
    'author': 'Jack Adamson',
    'author_email': 'jack@mrfluffybunny.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
