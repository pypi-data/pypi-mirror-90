# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weo']

package_data = \
{'': ['*']}

install_requires = \
['iso3166>=1.0.1,<2.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'pandas>=1.2.0,<2.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'weo',
    'version': '0.5.0',
    'description': 'Python client to download IMF World Economic Outlook (WEO) dataset as pandas dataframes.',
    'long_description': None,
    'author': 'Evgeny Pogrebnyak',
    'author_email': 'e.pogrebnyak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
