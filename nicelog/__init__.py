import logging
import sys


def setup_logging(debug=False):
    """Helper function to quickly setup everything needed.

    Configures the logging system to print colorful messages to the
    standard error.

    Args:

        debug:
            If set to True, will use DEBUG as log level for the "root"
            logger.  Otherwise, it will default to INFO.
    """

    from nicelog.formatters import Colorful
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(Colorful(
        show_date=True,
        show_function=True,
        show_filename=True,
        message_inline=False))
    handler.setLevel(logging.DEBUG)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if debug else logging.INFO)
    root_logger.addHandler(handler)
