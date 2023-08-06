# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seghouse',
 'seghouse.config',
 'seghouse.jobs',
 'seghouse.util',
 'seghouse.warehouse']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'black>=20.8b1,<21.0',
 'click>=7.1.2,<8.0.0',
 'clickhouse-driver[lz4,numpy,zstd]>=0.2.0,<0.3.0',
 'pandas>=1.2.0,<2.0.0',
 'pyhumps>=1.6.1,<2.0.0',
 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['seghouse = seghouse.app:app']}

setup_kwargs = {
    'name': 'seghouse',
    'version': '0.7.0',
    'description': '',
    'long_description': None,
    'author': 'Dinesh Sawant',
    'author_email': 'dineshsawant300@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
