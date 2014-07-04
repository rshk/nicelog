from nicelog.formatters import ColorLineFormatter
import logging
import sys

logger = logging.getLogger('foo')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(
    ColorLineFormatter(show_date=True, show_function=True,
                       show_filename=True))
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)


def do_stuff():
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')
    try:
        raise ValueError("Example exception")
    except:
        logger.exception("An error happened")


do_stuff()
