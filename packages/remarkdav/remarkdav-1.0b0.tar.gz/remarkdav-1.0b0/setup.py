# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['remarkdav']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'dateparser>=1.0.0,<2.0.0',
 'dynaconf>=3.1.2,<4.0.0',
 'fpdf>=1.7.2,<2.0.0',
 'peewee>=3.14.0,<4.0.0',
 'rmapy>=0.2.2,<0.3.0',
 'tabulate>=0.8.7,<0.9.0',
 'webdavclient3>=3.14.5,<4.0.0']

entry_points = \
{'console_scripts': ['remarkdav = remarkdav.cli:cli']}

setup_kwargs = {
    'name': 'remarkdav',
    'version': '1.0b0',
    'description': 'A tool to sync webdav files (only PDF) to the reMarkable cloud',
    'long_description': None,
    'author': 'Jonathan Weth',
    'author_email': 'dev@jonathanweth.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
