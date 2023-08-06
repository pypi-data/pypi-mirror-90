# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ni_python_styleguide']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0',
 'click>=7.1.2,<8.0.0',
 'flake8-black>=0.2.1,<0.3.0',
 'flake8>=3.8.3,<4.0.0',
 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['ni-python-styleguide = ni_python_styleguide._cli:main']}

setup_kwargs = {
    'name': 'ni-python-styleguide',
    'version': '0.1.2',
    'description': "NI's internal and external Python linter rules and plugins",
    'long_description': None,
    'author': 'NI',
    'author_email': 'opensource@ni.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
