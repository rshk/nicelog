import os
import logging
import sys

from termcolor import colored

POWERLINE_STYLE = os.environ.get('HAS_POWERLINE_FONT', False)


class ColorLineFormatter(logging.Formatter):
    level_colors = {
        logging.DEBUG: 'cyan',
        logging.INFO: 'green',
        logging.WARNING: 'yellow',
        logging.ERROR: 'red',
        logging.CRITICAL: 'red',
    }

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

    def format(self, record):
        """Format logs nicely"""

        color = self.level_colors.get(record.levelno, 'white')

        levelname = colored(' {0:<6} '.format(record.levelname),
                            color, attrs=['reverse'])

        if POWERLINE_STYLE:
            levelname += colored(u'\ue0b0', color, 'on_white')

        loggername = colored(' {0} '.format(record.name), 'red', 'on_white')

        if POWERLINE_STYLE:
            loggername += colored(u'\ue0b0', 'white')

        message = colored(record.getMessage(), color)

        s = ' '.join((''.join((levelname, loggername)), message))

        exc_info = self._get_exc_info(record)
        if exc_info is not None:
            if s[-1:] != "\n":
                s = s + "\n"
            s += colored(exc_info, 'grey', attrs=['bold'])

        return s
