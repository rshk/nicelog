# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals

from nicelog.formatters import Colorful
from nicelog.colorers.terminal import Xterm16Colorer, Xterm256Colorer


class TestColorfulFormatter(object):

    def test_debug_messages_are_rendered_properly(self):
        formatter = Colorful()

        msg = formatter.format()
        pass
    pass
