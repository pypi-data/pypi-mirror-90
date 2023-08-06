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
    'version': '0.1.2',
    'description': 'simple colorized log',
    'long_description': 'sclog - simple colorized log\n============================\n\nRationale\n---------\nPython has a pretty convenient [logging framework built-in](https://docs.python.org/3/howto/logging.html), which makes it super easy to get started:\n\n```python\nimport logging\n\nlogging.warning("That was easy")\n```\n\nOr, if you have a few different files in your project and want to distinguish between them:\n\n```python\nimport logging\n\nlogger = logging.getLogger(__name__)\n\nlogger.error("Uh oh, something bad happened")\n```\n\nBut, there are a few annoyances.\n\nFirst, as [the documentation explains](https://docs.python.org/3/howto/logging.html#a-simple-example), **debug and info messages aren\'t shown with the default log level**.\nWant to add a quick `logging.debug` message to your scripts? You\'ll need to configure a log formatter first.\n\nSecond, the **default log formatting is missing some information like the timestamp**.\nThe default output looks something like this:\n\n```\nWARNING:root:your warning message\n```\n\n...and if you want it to look differently, you again need a custom formatter.\n\nThis library\n------------\nThis library exists, to be honest, for my own convenience. Its purpose it to provide some useful (to me) defaults as a *very* light-weight layer on top of Python\'s default logging framework.\nSpecifically, it:\n\n1. Sets the default log level to `DEBUG`\n2. Uses a formatter that includes the timestamp\n3. (Optionally) colorizes the output using [colorlog](https://github.com/borntyping/python-colorlog) (another task that normally requires creating a custom formatter)\n\nUsage\n-----\nThe "API" for this library is meant to be maximally compatible with the built-in logging API.\nLike Python\'s `logging` module, it exposes a `getLogger` function that you call with a string (the name).\nThis returns a [standard Logger object](https://docs.python.org/3/howto/logging.html#loggers) that you use in a familiar way.\n\n```python\nfrom sclog import getLogger\n\nlogger = getLogger(__name__)\n\nlogger.info("Hello, %s!", "world")\n```\n\nThis outputs (in a nice green color):\n\n```\n2021-01-01 00:00:00:00,000 - __main__ - DEBUG - Hello, world!\n```\n\nInstallation\n------------\n\n    pip install sclog\n    pip install colorlog  # optional, include if you want colors\n\n\nYou can also just copy [the file](sclog/sclog.py) into your own project.\n',
    'author': 'nmalkin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nmalkin/sclog',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
