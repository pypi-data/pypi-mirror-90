# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scatsutilities']

package_data = \
{'': ['*']}

install_requires = \
['geopandas>=0.8.1,<0.9.0']

setup_kwargs = {
    'name': 'scatsutilities',
    'version': '0.1.0',
    'description': 'Python package providing utilities to process SCATS traffic system data',
    'long_description': None,
    'author': 'John Trieu',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
