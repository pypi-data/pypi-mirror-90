# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sclog']

package_data = \
{'': ['*']}

extras_require = \
{'color': ['colorlog>=4.6.2,<5.0.0']}

setup_kwargs = {
    'name': 'sclog',
    'version': '0.1.1',
    'description': 'simple colorized log',
    'long_description': None,
    'author': 'nmalkin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
