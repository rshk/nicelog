import logging
import sys

from nicelog.formatters import Colorful

logger = logging.getLogger('foo')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(Colorful())
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)


def first_wrapper():
    local_1st_1 = 'Value of first local var'  # noqa
    local_1st_2 = 1234  # noqa
    second_wrapper()


def second_wrapper():
    local_2nd_1 = True  # noqa
    local_2nd_2 = u'Something different'  # noqa
    some_function()


def some_function():
    func_local = {'Hello': 'World'}  # noqa
    raise ValueError('This is an exception')


def do_stuff():
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')
    try:
        first_wrapper()
    except:
        logger.exception("An error occurred")


do_stuff()
