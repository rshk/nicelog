Nice Log
########

Provide formatters to nicely display colorful logging output on the console.

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

.. image:: https://raw.githubusercontent.com/rshk/nicelog/master/.screenshots/nicelog2.png
    :alt: Screenshot


Powerline font support
======================

You can set the ``HAS_POWERLINE_FONT`` environment variable to a
non-null value in order to tell the formatter to use powerline-style
symbols (specifically, the "arrow" thing).
