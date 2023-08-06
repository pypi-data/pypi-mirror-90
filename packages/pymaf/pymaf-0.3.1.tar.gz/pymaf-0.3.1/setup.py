# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymaf']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.4,<2.0.0', 'repos>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'pymaf',
    'version': '0.3.1',
    'description': 'A toolbox for extracting signals from timeseries',
    'long_description': None,
    'author': 'Matz Haugen',
    'author_email': 'matzhaugen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}
from setup import *
build(setup_kwargs)

setup(**setup_kwargs)
