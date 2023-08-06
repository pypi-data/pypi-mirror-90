# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wutch']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=3.141.0,<4.0.0', 'watchdog>=1.0.2,<2.0.0']

entry_points = \
{'console_scripts': ['wutch = wutch.app:cli']}

setup_kwargs = {
    'name': 'wutch',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'vduseev',
    'author_email': 'vagiz@duseev.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
