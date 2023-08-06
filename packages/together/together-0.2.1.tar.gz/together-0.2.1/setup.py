# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['together']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'pluggy>=0.13.1,<0.14.0']

setup_kwargs = {
    'name': 'together',
    'version': '0.2.1',
    'description': 'Pluggable CLIs with click and pluggy',
    'long_description': None,
    'author': 'Stephen Rosen',
    'author_email': 'sirosen@globus.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
