# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asff']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'asff',
    'version': '0.1.1',
    'description': 'asff is a Python library to work with Amazon Security Finding Format',
    'long_description': '# python-asff\n[![build](https://github.com/xen0l/python-asff/workflows/Python%20package/badge.svg?branch=master)](https://github.com/xen0l/python-asff/actions)\n[![codecov](https://codecov.io/gh/xen0l/python-asff/branch/master/graph/badge.svg?token=GEFB001RIX)](https://codecov.io/gh/xen0l/python-asff)\n[![Documentation Status](https://readthedocs.org/projects/python-asff/badge/?version=latest)](https://python-asff.readthedocs.io/en/latest/?badge=latest)\n\nPython library to work with Amazon Security Finding Format (ASFF)',
    'author': 'Adam Števko',
    'author_email': 'adam.stevko@gmail.com',
    'maintainer': 'Adam Števko',
    'maintainer_email': 'adam.stevko@gmail.com',
    'url': 'https://github.com/xen0l/python-asff',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
