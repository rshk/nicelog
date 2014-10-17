Nice Log
########

.. image:: https://travis-ci.org/rshk/nicelog.svg?branch=master
    :target: https://travis-ci.org/rshk/nicelog

.. image:: https://coveralls.io/repos/rshk/nicelog/badge.png
    :target: https://coveralls.io/r/rshk/nicelog

.. image:: https://pypip.in/version/nicelog/badge.svg?text=version
    :target: https://github.com/rshk/nicelog.git
    :alt: Latest PyPI version

.. image:: https://pypip.in/download/nicelog/badge.svg?period=month
    :target: https://github.com/rshk/nicelog.git
    :alt: Number of PyPI downloads

.. image:: https://pypip.in/py_versions/nicelog/badge.svg
    :target: https://pypi.python.org/pypi/nicelog/
    :alt: Supported Python versions

.. image:: https://pypip.in/status/nicelog/badge.svg
    :target: https://pypi.python.org/pypi/nicelog/
    :alt: Development Status

.. image:: https://pypip.in/license/nicelog/badge.svg
    :target: https://pypi.python.org/pypi/nicelog/
    :alt: License

Provide formatters to nicely display colorful logging output on the console.

`Fork this project on GitHub <https://github.com/rshk/nicelog>`_

Right now, it contains only one formatter, coloring log lines
depending on the log level and adding nice line prefixes containing
logger name, but future plans are to add more formatters and allow
better ways to customize them.


Example usage
=============

.. code-block:: python

    from nicelog.formatters import ColorLineFormatter
    import logging
    import sys

    logger = logging.getLogger('foo')
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(ColorLineFormatter())
    handler.setLevel(logging.DEBUG)

    logger.addHandler(handler)

    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')


Example output
==============

Here it is, in all its glory:

.. image:: https://raw.githubusercontent.com/rshk/nicelog/master/.screenshots/nicelog2.png?v=1
    :alt: Screenshot

If you want to see what it looks like in 256color mode, with all the fields enabled:

.. image:: https://raw.githubusercontent.com/rshk/nicelog/master/.screenshots/nicelog3.png?v=2
    :alt: Screenshot


Powerline font support
======================

You can set the ``HAS_POWERLINE_FONT`` environment variable to a
non-null value in order to tell the formatter to use powerline-style
symbols (specifically, the "arrow" thing).

