# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dtb', 'dtb.money']

package_data = \
{'': ['*']}

install_requires = \
['dtb.currency>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'dtb.money',
    'version': '1.1.1',
    'description': 'Simple money implementation',
    'long_description': None,
    'author': 'Dima Doroshev',
    'author_email': 'dima@doroshev.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
