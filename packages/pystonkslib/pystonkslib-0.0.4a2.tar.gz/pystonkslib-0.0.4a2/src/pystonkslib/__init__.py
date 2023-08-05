"""Configs for the library."""

import logging
import logging.config
import os

LIBRARY_NAME = os.path.basename(os.path.dirname(__file__))

# Formats for logging
LOGGING_DATE_FORMAT = "%m/%d/%Y %I:%M:%S %p"
NORMAL_LOGGING_FORMAT = "%(asctime)s %(levelname)-8s [%(name)s] %(message)s"
VERBOSE_LOGGING_FORMAT = "%(asctime)s %(levelname)-8s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"

# Configurable logging settings
LOGGING_LEVEL = os.environ.get(f"{LIBRARY_NAME.upper()}_LOGGING_LEVEL", logging.INFO)
LOGGING_FORMATTER = os.environ.get(f"{LIBRARY_NAME.upper()}_LOGGING_VERBOSITY", "normal")

# General logging config here.
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {"datefmt": LOGGING_DATE_FORMAT, "format": VERBOSE_LOGGING_FORMAT,},
        "normal": {"datefmt": LOGGING_DATE_FORMAT, "format": NORMAL_LOGGING_FORMAT,},
    },
    "handlers": {
        "console": {"level": LOGGING_LEVEL, "class": "logging.StreamHandler", "formatter": LOGGING_FORMATTER,},
        "null": {"level": LOGGING_LEVEL, "class": "logging.NullHandler", "formatter": LOGGING_FORMATTER,},
    },
    "loggers": {LIBRARY_NAME: {"handlers": ["console"], "level": LOGGING_LEVEL,},},
}

# Configure the logging, and then log a message after import of the library.
logging.config.dictConfig(LOGGING_CONFIG)
LOGGER = logging.getLogger(LIBRARY_NAME)
LOGGER.info("Loaded %s library.", LIBRARY_NAME)
