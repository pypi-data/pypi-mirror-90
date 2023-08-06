sclog - simple colorized log
============================

Rationale
---------
Python has a pretty convenient [logging framework built-in](https://docs.python.org/3/howto/logging.html), which makes it super easy to get started:

```python
import logging

logging.warning("That was easy")
```

Or, if you have a few different files in your project and want to distinguish between them:

```python
import logging

logger = logging.getLogger(__name__)

logger.error("Uh oh, something bad happened")
```

But, there are a few annoyances.

First, as [the documentation explains](https://docs.python.org/3/howto/logging.html#a-simple-example), **debug and info messages aren't shown with the default log level**.
Want to add a quick `logging.debug` message to your scripts? You'll need to configure a log formatter first.

Second, the **default log formatting is missing some information like the timestamp**.
The default output looks something like this:

```
WARNING:root:your warning message
```

...and if you want it to look differently, you again need a custom formatter.

This library
------------
This library exists, to be honest, for my own convenience. Its purpose it to provide some useful (to me) defaults as a *very* light-weight layer on top of Python's default logging framework.
Specifically, it:

1. Sets the default log level to `DEBUG`
2. Uses a formatter that includes the timestamp
3. (Optionally) colorizes the output using [colorlog](https://github.com/borntyping/python-colorlog) (another task that normally requires creating a custom formatter)

Usage
-----
The "API" for this library is meant to be maximally compatible with the built-in logging API.
Like Python's `logging` module, it exposes a `getLogger` function that you call with a string (the name).
This returns a [standard Logger object](https://docs.python.org/3/howto/logging.html#loggers) that you use in a familiar way.

```python
from sclog import getLogger

logger = getLogger(__name__)

logger.info("Hello, %s!", "world")
```

This outputs (in a nice green color):

```
2021-01-01 00:00:00:00,000 - __main__ - DEBUG - Hello, world!
```

Installation
------------

    pip install sclog
    pip install colorlog  # optional, include if you want colors


You can also just copy [the file](sclog/sclog.py) into your own project.
