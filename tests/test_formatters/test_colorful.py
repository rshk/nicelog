# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals

from nicelog.formatters import Colorful
from nicelog.colorers.terminal import Xterm16Colorer, Xterm256Colorer
import logging
import re

import io
from logging import getLogger, StreamHandler, DEBUG
from freezegun import freeze_time


@freeze_time('2015-11-30 16:30')
class TestColorfulFormatter(object):

    def test_formatter_works_end_to_end(self):
        outstream = io.StringIO()
        handler = StreamHandler(outstream)
        handler.setLevel(DEBUG)
        formatter = Colorful()
        handler.setFormatter(formatter)
        logger = getLogger('test_logger')
        logger.setLevel(DEBUG)
        logger.addHandler(handler)

        logger.info('Hello, world')

        data = outstream.getvalue()
        assert '\x1b[' in data  # Make sure we have colors

        clean = re.sub('\x1b\[.*?m', '', data)
        assert clean == (
            '   INFO    2015-11-30 16:30:00  test_logger  test_colorful.py:28 '
            'test_colorful.test_formatter_works_end_to_end \n'
            '    Hello, world\n')
