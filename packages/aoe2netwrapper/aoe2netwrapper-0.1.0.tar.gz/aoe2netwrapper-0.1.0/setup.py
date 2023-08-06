# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aoe2netwrapper']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'aoe2netwrapper',
    'version': '0.1.0',
    'description': 'My Python wrapper for the aoe2.net data API',
    'long_description': None,
    'author': 'Felix Soubelet',
    'author_email': 'felix.soubelet@liverpool.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
