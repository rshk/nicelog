# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals


class BaseStyle(object):

    date = dict(fg='cyan')

    level_name_DEBUG = dict(fg='cyan', attrs=['reverse'])
    level_name_INFO = dict(fg='green', attrs=['reverse'])
    level_name_WARNING = dict(fg='yellow', attrs=['reverse'])
    level_name_ERROR = dict(fg='red', attrs=['reverse'])
    level_name_CRITICAL = dict(fg='red', attrs=['reverse'])
    level_name_DEFAULT = dict(fg='white', attrs=['reverse'])

    logger_name = dict(fg='red', bg='white')
    file_name = dict(fg='green')
    line_number = dict(fg='hi_green')
    module_name = dict(fg='yellow')
    function_name = dict(fg='hi_yellow')

    message_DEBUG = dict(fg='cyan')
    message_INFO = dict(fg='green')
    message_WARNING = dict(fg='yellow')
    message_ERROR = dict(fg='red')
    message_CRITICAL = dict(fg='red')
    message_DEFAULT = dict(fg='white')

    exception = dict(fg='hi_grey')
