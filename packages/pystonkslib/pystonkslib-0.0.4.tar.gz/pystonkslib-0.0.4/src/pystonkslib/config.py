"""General config utilities for the pystonkslib library."""
import configparser
import logging
import os

LOGGER = logging.getLogger(__name__)
CONFIG_FILE_DEFAULT = """
[symbol_info]
filename = nasdaqlisted.txt
url = ftp.nasdaqtrader.com
directory = SymbolDirectory

"""


def get_config_folder() -> str:
    """Get or create the config folder and return it."""

    # Ensure we have a config path.
    config_path = os.path.join(os.path.expanduser("~"), ".pystonkslib")
    if not os.path.exists(config_path):
        LOGGER.info("%s doesn't exist - creating.", config_path)
        os.makedirs(config_path)
        LOGGER.info("Path %s created: %s", config_path, bool(os.path.exists(config_path)))

    return config_path


def get_data_folder() -> str:
    """Get or create the config folder and return it."""

    # Ensure we have a config path.
    # Make sure we have a data folder as well.
    data_folder = os.path.join(get_config_folder(), "data")
    if not os.path.exists(data_folder):
        LOGGER.info("No data path found - creating.")
        os.makedirs(data_folder)

    return data_folder


def get_config_file_path() -> str:
    """Get the config file path for pystonkslib package."""
    LOGGER.info("Attempting to get config file path.")
    config_folder = get_config_folder()
    config_file_name = "pystonkslib.ini"
    config_file_path = os.path.join(config_folder, config_file_name)
    LOGGER.info("Got config file path: %s", config_file_path)
    return config_file_path


def write_default_config() -> None:
    """Write the default config for pystonkslib package."""

    config_file_path = get_config_file_path()
    with open(config_file_path, "wt") as config_file:
        config_file.write(CONFIG_FILE_DEFAULT)
    LOGGER.info("Wrote default config file.")


def get_config() -> configparser.ConfigParser:
    """Get a config object for the pystonkslib package."""

    LOGGER.info("Getting config for pystonkslib")
    config_file_path = get_config_file_path()
    if not os.path.exists(config_file_path):
        LOGGER.info("No default config found - writing it.")
        write_default_config()
    LOGGER.info("Default config in place.")
    config = configparser.ConfigParser()
    LOGGER.info("Reading config file.")
    config.read(config_file_path)
    LOGGER.info("Config file read.")
    return config
