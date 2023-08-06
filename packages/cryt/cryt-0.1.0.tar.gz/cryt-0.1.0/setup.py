# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cryt', 'cryt.command']

package_data = \
{'': ['*']}

install_requires = \
['ccxt>=1.39.75,<2.0.0', 'fire>=0.3.1,<0.4.0', 'rich>=9.5.1,<10.0.0']

entry_points = \
{'console_scripts': ['cryt = cryt.main:main']}

setup_kwargs = {
    'name': 'cryt',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'atsuhiro-narita',
    'author_email': 'alayashiki@gmail.com',
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
