import datetime
import logging
import os
import sys


POWERLINE_STYLE = bool(os.environ.get('HAS_POWERLINE_FONT', False))


class BaseColorer(object):
    def colorize(self, text, fg=None, bg=None, attrs=None):
        return text


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
        _open_parts = filter(None, _open_parts)
        if len(_open_parts) == 0:
            _open_parts.append(self._reset)
        t_open = '\033[{0}m'.format(';'.join(str(x) for x in _open_parts))
        t_close = '\033[{0}m'.format(self._reset)
        return u'{0}{1}{2}'.format(t_open, text, t_close)


class Xterm256Colorer(Xterm16Colorer):
    _colors = dict(
        grey='240',
        red='196',
        green='70',
        yellow='202',
        blue='33',
        magenta='207',
        cyan='37',
        white='252',
        hi_grey='245',
        hi_red='203',
        hi_green='190',
        hi_yellow='214',
        hi_blue='75',
        hi_magenta='199',
        hi_cyan='116',
        hi_white='255')

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


class ColorLineFormatter(logging.Formatter):
    level_colors = {
        logging.DEBUG: 'cyan',
        logging.INFO: 'green',
        logging.WARNING: 'yellow',
        logging.ERROR: 'red',
        logging.CRITICAL: 'red',
    }

    def __init__(self, show_date=False, show_function=False,
                 show_filename=False, colorer=None, *a, **kw):
        super(ColorLineFormatter, self).__init__(*a, **kw)
        if colorer is None:
            colorer = self._get_colorer()
        self._colorer = colorer
        self._show_date = show_date
        self._show_function = show_function
        self._show_filename = show_filename

    def _get_colorer(self):
        if os.environ.get('ANSI_COLORS_DISABLED') is not None:
            return None
        term = os.environ.get('TERM')
        if '256color' in term:
            return Xterm256Colorer()
        return Xterm16Colorer()

    def _get_exc_info(self, record):
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
                return record.exc_text.decode(sys.getfilesystemencoding(),
                                              'replace')
        return None

    def _colorize(self, text, fg=None, bg=None, attrs=None):
        if self._colorer is None:
            return text
        return self._colorer.colorize(text, fg=fg, bg=bg, attrs=attrs)

    def _format_date(self, record):
        fmtdate = datetime.datetime.fromtimestamp(
            record.created).strftime("%F %T")
        return self._colorize(fmtdate, attrs=['bold'])

    def _format_level_and_name(self, record):
        color = self.level_colors.get(record.levelno, 'white')
        levelname = self._colorize(
            ' {0:<6} '.format(record.levelname),
            fg=color, attrs=['reverse'])
        if POWERLINE_STYLE:
            levelname += self._colorize(u'\ue0b0', fg=color, bg='white')

        loggername = self._colorize(
            ' {0} '.format(record.name), fg='red', bg='white')
        if POWERLINE_STYLE:
            loggername += self._colorize(u'\ue0b0', 'white')

        return levelname + loggername

    def _format_filename(self, record):
        return ':'.join((
            self._colorize(record.filename, fg='green'),
            self._colorize(str(record.lineno), fg='hi_green'),
        ))

    def _format_function(self, record):
        return '.'.join((
            self._colorize(record.module, fg='yellow'),
            self._colorize(str(record.funcName), fg='hi_yellow'),
        ))

    def format(self, record):
        """Format logs nicely"""

        parts = []

        if self._show_date:
            parts.append(self._format_date(record))

        parts.append(self._format_level_and_name(record))

        if self._show_filename:
            parts.append(self._format_filename(record))

        if self._show_function:
            parts.append(self._format_function(record))

        color = self.level_colors.get(record.levelno, 'white')
        parts.append(self._colorize(record.getMessage().rstrip(), color))

        exc_info = self._get_exc_info(record)
        if exc_info is not None:
            parts.append(
                "\n" + self._colorize(exc_info, fg='hi_grey'))

        return ' '.join(parts)
