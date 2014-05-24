# Nice Log

Provide formatters to nicely display colorful logging output on the console.

## Example usage

```python
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
```

## Powerline font support

You can set the ``HAS_POWERLINE_FONT`` environment variable to a
non-null value in order to tell the formatter to use powerline-style
symbols.
