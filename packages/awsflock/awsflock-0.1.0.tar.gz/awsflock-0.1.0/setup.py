# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awsflock']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.47,<2.0.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['awsflock = awsflock:cli']}

setup_kwargs = {
    'name': 'awsflock',
    'version': '0.1.0',
    'description': 'Simple locking in AWS',
    'long_description': None,
    'author': 'Stephen Rosen',
    'author_email': 'sirosen@globus.org',
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
