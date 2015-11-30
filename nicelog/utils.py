# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import io
import linecache
import sys

import six
from six.moves import zip, range


def trim_string(s, maxlen=1024, ellps='...'):
    """
    Trim a string to a maximum length, adding an "ellipsis"
    indicator if the string was trimmed
    """

    # todo: allow cutting in the middle of the string,
    #       instead of just on the right end..?

    if len(s) > maxlen:
        return s[:maxlen - len(ellps)] + ellps
    return s


class FrameInfo(object):
    def __init__(self, filename, lineno, name, line, locs):
        self.filename = filename
        self.lineno = lineno
        self.name = name
        self.line = line
        self.locs = self._format_locals(locs)
        self.context = self._get_context()

    def _get_context(self, size=3):
        """Return some "context" lines from a file"""
        _start = max(0, self.lineno - size - 1)
        _end = self.lineno + size
        _lines = linecache.getlines(self.filename)[_start:_end]
        _lines = [x.rstrip() for x in _lines]
        _lines = list(zip(range(_start + 1, _end + 1), _lines))
        return _lines

    def _format_locals(self, locs):
        formatted = {}
        for k, v in six.iteritems(locs):
            try:
                fmtval = trim_string(repr(v), maxlen=1024)
            except Exception as e:
                fmtval = '<Error creating repr(): {0}>'.format(repr(e))
            formatted[k] = fmtval
        return formatted


class TracebackInfo(object):
    """
    Class used to hold information about an error traceback.

    This is meant to be serialized & stored in the database, instead
    of a full traceback object, which is *not* serializable.

    It holds information about:

    - the exception that caused the thing to fail
    - the stack frames (with file / line number, function and exact code
      around the point in which the exception occurred)
    - a representation of the local variables for each frame.

    A textual representation of the traceback information may be
    retrieved by using ``str()`` or ``unicode()`` on the object
    instance.
    """

    def __init__(self):
        self.frames = []

    @classmethod
    def from_current_exc(cls):
        """
        Instantiate with traceback from ``sys.exc_info()``.
        """
        return cls.from_tb(sys.exc_info()[2])

    @classmethod
    def from_tb(cls, tb):
        """
        Instantiate from a traceback object.
        """
        obj = cls()
        obj.frames = cls._extract_tb(tb)
        return obj

    def format(self):
        """Format traceback for printing"""

        output = io.StringIO()
        output.write('------------------ '
                     'Traceback (most recent call last) '
                     '-----------------\n\n')
        output.write('\n'.join(
            self._format_frame(f)
            for f in self.frames))
        return output.getvalue()

    def format_color(self):  # todo: accept a colorizer + style
        """Format traceback for printing on 256-color terminal"""

        output = io.StringIO()
        output.write('\033[0m------------------ '
                     'Traceback (most recent call last) '
                     '-----------------\n\n')
        output.write(u'\n'.join(
            self._format_frame_color(f)
            for f in self.frames))
        return output.getvalue()

    def _format_frame(self, frame):
        output = io.StringIO()
        output.write(
            u'  File "{0}", line {1}, in {2}\n'.format(
                frame.filename, frame.lineno, frame.name))

        if frame.context:
            for line in frame.context:
                fmtstring = u'{0:4d}: {1}\n'
                if line[0] == frame.lineno:
                    fmtstring = u'    > ' + fmtstring
                else:
                    fmtstring = u'      ' + fmtstring
                output.write(fmtstring.format(line[0], line[1]))

        if len(frame.locs):
            output.write(u'\n      Local variables:\n')

            for key, val in sorted(six.iteritems(frame.locs)):
                output.write(u'        {0} = {1}\n'.format(key, val))

        return output.getvalue()

    def _format_frame_color(self, frame):
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import Terminal256Formatter

        _code_lexer = get_lexer_by_name('python')
        _code_formatter = Terminal256Formatter(style='monokai')

        def _highlight(code):
            return highlight(code, _code_lexer, _code_formatter)

        output = io.StringIO()
        output.write(
            u'\033[0m'
            u'\033[1mFile\033[0m \033[38;5;70m"{0}"\033[39m, '
            u'\033[1mline\033[0m \033[38;5;190m{1}\033[39m, '
            u'\033[1min\033[0m \033[38;5;214m{2}\033[0m\n\n'
            .format(frame.filename, frame.lineno, frame.name))

        if frame.context:
            for line in frame.context:
                fmtstring = u'{0:4d}: {1}\n'
                if line[0] == frame.lineno:
                    fmtstring = (u'    \033[48;5;250m\033[38;5;232m'
                                 u'{0:4d}\033[0m {1}\n')
                else:
                    fmtstring = (u'    \033[48;5;237m\033[38;5;250m'
                                 u'{0:4d}\033[0m {1}\n')

                color_line = _highlight(line[1])
                output.write(fmtstring.format(line[0], color_line.rstrip()))

        if len(frame.locs):
            output.write(u'\n    \033[1mLocal variables:\033[0m\n')

            for key, val in sorted(six.iteritems(frame.locs)):
                code_line = _highlight(u'{0} = {1}'.format(key, val)).rstrip()
                output.write(u'      {0}\n'.format(code_line))

        return output.getvalue()

    @classmethod
    def _extract_tb(cls, tb, limit=None):
        if limit is None:
            if hasattr(sys, 'tracebacklimit'):
                limit = sys.tracebacklimit
        frames = []
        n = 0
        while tb is not None and (limit is None or n < limit):
            f = tb.tb_frame
            lineno = tb.tb_lineno
            co = f.f_code
            filename = co.co_filename
            name = co.co_name
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            locs = f.f_locals  # Will be converted to repr() by FrameInfo
            if line:
                line = line.strip()
            else:
                line = None
            frames.append(FrameInfo(filename, lineno, name, line, locs))
            tb = tb.tb_next
            n = n+1
        return frames

    def __str__(self):
        return self.format().encode('utf-8')

    def __unicode__(self):
        return self.format()
