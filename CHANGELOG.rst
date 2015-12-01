Changelog
=========

v0.2
----

- More decoupling between "colorer" and "style"
- Support for pretty tracebacks (colorful + code context + locals)
- Added some tests
- Python3 support via six


v0.1.9
------

- Replaced ``strftime(3)`` conversion specifiers ``%F`` and ``%T``
  aren't available on all platforms: replaced with long versions
  ``%Y-%m-%d`` and ``%H:%M:%S``.


v0.1.8
------

- Prevent failure in case the ``TERM`` environment variable is not set (PR #1)


v0.1.7
------

- Added support for ``message_inline`` argument. If set to ``False``,
  messages will be displayed on their own line (useful when enabling a lot of
  information)


v0.1.6
------

- Added support for showing more information:

  - record date
  - file name / line number
  - module / function


v0.1.5
------

- Added support for nicer colors in 256-color mode
- Removed dependency from termcolor (now shipping better implementation)
