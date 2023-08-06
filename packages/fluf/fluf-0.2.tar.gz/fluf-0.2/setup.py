# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fluf', 'fluf.cli', 'fluf.etc', 'fluf.plugin']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'configobj>=5.0.6,<6.0.0',
 'dill>=0.3.3,<0.4.0',
 'humanfriendly>=9.1,<10.0',
 'matplotlib>=3.3.3,<4.0.0',
 'networkx>=2.5,<3.0',
 'peewee>=3.14.0,<4.0.0',
 'pluggy>=0.13.1,<0.14.0',
 'rich>=9.5.1,<10.0.0',
 'strictyaml>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'fluf',
    'version': '0.2',
    'description': 'Simple caching & workflow',
    'long_description': None,
    'author': 'Mark Fiers',
    'author_email': 'mark.fiers.42@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
