# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datamerger']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.0,<2.0.0', 'tqdm>=4.55.1,<5.0.0']

setup_kwargs = {
    'name': 'datamerger',
    'version': '0.1.4',
    'description': 'Quick tools to easily merge multiple, multi-dimensional datasets based on arbitrary attributes and criteria.',
    'long_description': None,
    'author': 'Max Fan',
    'author_email': 'theinnovativeinventor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
