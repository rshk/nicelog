# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals

import io
import re
from logging import DEBUG, StreamHandler, getLogger

import pytest
from freezegun import freeze_time

from nicelog.formatters import Colorful


@freeze_time('2015-11-30 16:30')
class TestColorfulFormatter(object):

    @pytest.fixture
    def logger_output(self):
        return io.StringIO()

    @pytest.fixture
    def logger(self, logger_output):
        handler = StreamHandler(logger_output)
        handler.setLevel(DEBUG)
        formatter = Colorful()
        handler.setFormatter(formatter)
        logger = getLogger('test_logger')
        logger.setLevel(DEBUG)
        logger.addHandler(handler)
        return logger

    def test_formatter_works_end_to_end(self, logger, logger_output):

        logger.info('Hello, world')

        data = logger_output.getvalue()

        # Make sure we have colors, but don't bother matching them
        assert '\x1b[' in data

        RE_EXPECTED = re.compile(
            r'^   INFO    '
            r'2015-11-30 16:30:00  '
            r'test_logger  '
            r'test_colorful.py:[0-9]+ '
            r'test_colorful.test_formatter_works_end_to_end \n'
            r'    Hello, world\n$')

        clean = re.sub('\x1b\[.*?m', '', data)
        assert RE_EXPECTED.match(clean)

    def test_debug_message_can_be_logged(self, logger, logger_output):

        logger.debug('Hello, world')

        data = logger_output.getvalue()

        assert '\x1b[' in data
        assert 'DEBUG' in data
        assert 'Hello, world' in data

    def test_warning_message_can_be_logged(self, logger, logger_output):

        logger.warning('Hello, world')

        data = logger_output.getvalue()

        assert '\x1b[' in data
        assert 'WARNING' in data
        assert 'Hello, world' in data

    def test_error_message_can_be_logged(self, logger, logger_output):

        logger.error('Hello, world')

        data = logger_output.getvalue()

        assert '\x1b[' in data
        assert 'ERROR' in data
        assert 'Hello, world' in data

    def test_exception_can_be_logged(self, logger, logger_output):

        try:
            raise ValueError('EXCEPTION_MESSAGE')
        except:
            logger.exception('Hello, world')

        data = logger_output.getvalue()

        assert '\x1b[' in data
        assert 'EXCEPTION' in data
        assert 'Hello, world' in data
        assert 'EXCEPTION_MESSAGE' in data
