import logging

__version__ = "0.0.1"
__release__ = __version__

DEBUG = False

LOG_FMT = (
    "%(levelname)s: %(name)s [%(process)d] {%(filename)s@L%(lineno)d}: %(message)s"
)
LOG_LVL = logging.INFO
