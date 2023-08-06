# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grunnlag']

package_data = \
{'': ['*']}

install_requires = \
['bergen>=0.1.4,<0.2.0',
 'dask[complete]>=2020.12.0,<2021.0.0',
 's3fs>=0.5.1,<0.6.0',
 'xarray[complete]>=0.16.2,<0.17.0',
 'zarr>=2.6.1,<3.0.0']

setup_kwargs = {
    'name': 'grunnlag',
    'version': '0.1.3',
    'description': 'Basic Schema for interacting with Arnheim through Bergen',
    'long_description': None,
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
