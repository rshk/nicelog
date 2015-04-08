# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals


class BaseColorer(object):
    def __init__(self, style):
        self.style = style

    def render(self, style, text):
        item_style = self._get_style(style)
        return self.colorize(text, **item_style)

    def _get_style(self, style_name):
        if isinstance(style_name, basestring):
            style_name = [style_name]
        for name in style_name:
            try:
                return getattr(self.style, name)
            except:
                pass
        return {}

    def colorize(self, text, fg=None, bg=None, attrs=None):
        return text
