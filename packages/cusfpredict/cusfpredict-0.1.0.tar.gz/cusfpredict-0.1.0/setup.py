# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cusfpredict']

package_data = \
{'': ['*']}

install_requires = \
['cfgrib>=0.9.8,<0.10.0',
 'fastkml>=0.11,<0.12',
 'numpy>=1.17,<2.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytz>=2020.5,<2021.0',
 'requests>=2.25.1,<3.0.0',
 'shapely>=1.7.1,<2.0.0',
 'xarray>=0.16.2,<0.17.0']

setup_kwargs = {
    'name': 'cusfpredict',
    'version': '0.1.0',
    'description': 'CUSF Predictor Wrapper & GFS Downloader',
    'long_description': None,
    'author': 'Mark Jessop',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
