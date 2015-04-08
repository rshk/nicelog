# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import datetime
import logging
import os
import sys

from nicelog.colorers.terminal import get_term_colorer
from nicelog.styles.base import BaseStyle as DefaultStyle


POWERLINE_STYLE = bool(os.environ.get('HAS_POWERLINE_FONT', False))
DEFAULT = object()


class Colorful(logging.Formatter):

    def __init__(self, show_date=True, show_function=True,
                 show_filename=True, message_inline=False,
                 beautiful_tracebacks=True,
                 colorer=DEFAULT, style=DEFAULT, *a, **kw):

        """Log formatter for beautiful colored output

        Args
            show_date: whether to include date in log output
            show_function: whether to include function name
            show_filename: whether to include file name
            message_inline: whether to print messages inline
            beautiful_tracebacks: whether to nicely format tracebacks
            colorer (BaseColorer): used to create color output
            style (BaseStyle): color style to use
        """

        super(ColorLineFormatter, self).__init__(*a, **kw)
        if style is DEFAULT:
            style = DefaultStyle()
        self.style = style
        if colorer is DEFAULT:
            colorer = get_term_colorer(style=style)
        self.colorer = colorer
        self._show_date = show_date
        self._show_function = show_function
        self._show_filename = show_filename
        self._message_inline = message_inline
        self._beautiful_tracebacks = beautiful_tracebacks

    def format(self, record):

        parts = []

        parts.append(self._format_level(record))

        if self._show_date:
            parts.append(self._format_date(record))

        parts.append(self._format_name(record))

        if self._show_filename:
            parts.append(self._format_filename(record))

        if self._show_function:
            parts.append(self._format_function(record))

        if self._message_inline:
            parts.append(self._format_message_inline(record).rstrip())
        else:
            parts.append(self._format_message_block(record).rstrip())

        # todo: beautiful exceptions if required to
        exc_info = self._format_traceback(record)
        if exc_info is not None:
            parts.append("\n" + self._render('exception', exc_info))

        return ' '.join(parts)

    def _format_traceback(self, record):
        if record.exc_info:
            if self._beautiful_tracebacks:
                return self._format_beautiful_traceback(record)
            return self._format_plain_traceback(record)
        return None

    def _render(self, style_name, text):
        if self.colorer is None:
            return text
        return self.colorer.render(style_name, text)

    def _format_date(self, record):
        fmtdate = datetime.datetime.fromtimestamp(
            record.created).strftime("%Y-%m-%d %H:%M:%S")
        return self._render('date', fmtdate)

    def _format_level_and_name(self, record):
        return ''.join((self._format_level(record), self._format_name(record)))

    def _format_level(self, record):
        return self._render(
            ('level_name_{}'.format(record.levelname), 'level_name_DEFAULT'),
            ' {0:^8} '.format(record.levelname))

    def _format_name(self, record):
        return self._render('logger_name', ' {0} '.format(record.name))

    def _format_filename(self, record):
        return ':'.join((
            self._render('file_name', record.filename),
            self._render('line_number', str(record.lineno)),
        ))

    def _format_function(self, record):
        return '.'.join((
            self._render('module_name', record.module),
            self._render('function_name', str(record.funcName)),
        ))

    def _format_message_inline(self, record):
        return self._render(
            ('message_{}'.format(record.levelname), 'message_DEFAULT'),
            record.getMessage().rstrip())

    def _format_message_block(self, record):
        return "\n" + self._indent(record.getMessage())

    def _indent(self, text, tab="    ", level=1):
        _indent = tab * level
        lines = text.splitlines()
        indented = ["{}{}".format(_indent, line) for line in lines]
        return "\n".join(indented)

    def _format_plain_traceback(self, record):
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            try:
                return unicode(record.exc_text)
            except UnicodeError:
                # Sometimes filenames have non-ASCII chars, which can lead
                # to errors when s is Unicode and record.exc_text is str
                # See issue 8924.
                # We also use replace for when there are multiple
                # encodings, e.g. UTF-8 for the filesystem and latin-1
                # for a script. See issue 13232.
                return record.exc_text.decode(
                    sys.getfilesystemencoding(), 'replace')
        return None

    def _format_beautiful_traceback(self, record):
        if not record.exc_info:
            return
        from nicelog.utils import TracebackInfo
        # todo: use colorer to render traceback!
        # todo: use suitable pygments formatter for the colorer
        return TracebackInfo.from_tb(record.exc_info[2]).format_color()


ColorLineFormatter = Colorful
