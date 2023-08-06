# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['malariagen_data']

package_data = \
{'': ['*']}

install_requires = \
['dask[array]>=2.9.0,<3.0.0',
 'fsspec>=0.7.4,<0.8.0',
 'gcsfs>=0.6.2,<0.7.0',
 'pandas>=1.1.0,<2.0.0',
 'zarr>=2.4.0,<3.0.0']

setup_kwargs = {
    'name': 'malariagen-data',
    'version': '0.1.0a8',
    'description': 'A package for accessing MalariaGEN public data.',
    'long_description': None,
    'author': 'Alistair Miles',
    'author_email': 'alimanfoo@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
