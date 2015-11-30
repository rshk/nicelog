# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os

from .base import BaseColorer


def get_term_colorer(*a, **kw):
    if os.environ.get('ANSI_COLORS_DISABLED') is not None:
        return None
    term = os.environ.get('TERM')
    if term and '256color' in term:
        return Xterm256Colorer(*a, **kw)
    return Xterm16Colorer(*a, **kw)


class Xterm16Colorer(BaseColorer):
    _colors = dict(
        grey='0', red='1', green='2', yellow='3',
        blue='4', magenta='5', cyan='6', white='7',
        hi_grey='0', hi_red='1', hi_green='2', hi_yellow='3',
        hi_blue='4', hi_magenta='5', hi_cyan='6', hi_white='7')
    _reset = '0'
    _attrs = {
        'bold': '1', 'dark': '2', 'underline': '4', 'blink': '5',
        'reverse': '7', 'concealed': '8',
    }

    def _get_fg_color(self, color):
        fg_color = self._colors.get(color)
        if fg_color is None:
            return
        return '3{0}'.format(fg_color)

    def _get_bg_color(self, color):
        bg_color = self._colors.get(color)
        if bg_color is None:
            return
        return '4{0}'.format(bg_color)

    def colorize(self, text, fg=None, bg=None, attrs=None):
        _attrs = filter(None, (self._attrs.get(x) for x in (attrs or [])))
        _open_parts = list(_attrs)
        _open_parts.append(self._get_fg_color(fg))
        _open_parts.append(self._get_bg_color(bg))
        _open_parts = [x for x in _open_parts if x]

        if len(_open_parts) == 0:
            _open_parts.append(self._reset)
        t_open = '\033[{0}m'.format(';'.join(str(x) for x in _open_parts))
        t_close = '\033[{0}m'.format(self._reset)
        return u'{0}{1}{2}'.format(t_open, text, t_close)


def _256c(num):  # color
    return str(16 + int(num, 6))


def _256g(num):  # gray
    return str(231 + num)


class Xterm256Colorer(Xterm16Colorer):

    _colors = dict(
        grey=_256g(9),
        red=_256c('500'),
        green=_256c('130'),
        yellow=_256c('510'),
        blue=_256c('025'),
        magenta=_256c('515'),
        cyan=_256c('033'),
        white=_256g(21),
        hi_grey=_256g(14),
        hi_red=_256c('511'),
        hi_green=_256c('450'),
        hi_yellow=_256c('530'),
        hi_blue=_256c('135'),
        hi_magenta=_256c('503'),
        hi_cyan=_256c('244'),
        hi_white=_256g(24))

    def _get_fg_color(self, color):
        fg_color = self._colors.get(color)
        if fg_color is None:
            return
        return '38;5;{0}'.format(fg_color)

    def _get_bg_color(self, color):
        bg_color = self._colors.get(color)
        if bg_color is None:
            return
        return '48;5;{0}'.format(bg_color)
