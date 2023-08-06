# Standard imports
from logging.handlers import RotatingFileHandler
import logging
import datetime as dt
import re
import json
import tempfile
import os
from pkg_resources import resource_filename

# Misc
MAX_RECENT_PROJECTS = 5
MIN_COMPLETION_LETTERS = 1
DEFAULT_SELECTION_NAME = "variants"
# version from which database files are supported (included)
MIN_AUTHORIZED_DB_VERSION = "0.2.0"


# ACMG Classification
CLASSIFICATION = {
    0: "Unclassified",
    1: "Benin",
    2: "Likely benin",
    3: "Variant of uncertain significance",
    4: "Likely pathogen",
    5: "Pathogen",
}

CLASSIFICATION_ICONS = {
    0: 0xF03A1,
    1: 0xF03A4,
    2: 0xF03A7,
    3: 0xF03AA,
    4: 0xF03AD,
    5: 0xF03B1,
}

# Genotypes
GENOTYPE_ICONS = {-1: 0xF10D3, 0: 0xF0766, 1: 0xF0AA1, 2: 0xF0AA5}

GENOTYPE_DESC = {
    -1: "Unknown genotype",
    0: "Homozygous wild",
    1: "Heterozygous",
    2: "Homozygous muted",
}

# Paths
DIR_LOGS = tempfile.gettempdir() + "/"

DIR_ASSETS = resource_filename(__name__, "assets/")  # current package name
DIR_TRANSLATIONS = DIR_ASSETS + "i18n/"
DIR_FONTS = DIR_ASSETS + "fonts/"
DIR_ICONS = DIR_ASSETS + "icons/"
DIR_STYLES = DIR_ASSETS + "styles/"

BASIC_STYLE = "Bright"
FONT_FILE = DIR_FONTS + "materialdesignicons-webfont.ttf"

# Websites and variant query
WEBSITES_URLS = {
    "GenCards - The human gene database": "https://www.genecards.org/cgi-bin/carddisp.pl?gene={gene}",
    "Varsome - Genes": "https://varsome.com/gene/{gene}",
    "Varsome - Variants": "https://varsome.com/variant/hg19/{chr}-{pos}-{ref}-{alt}",
}

REPORT_BUG_URL = "https://github.com/labsquare/cutevariant/issues/new"
WIKI_URL = "https://github.com/labsquare/cutevariant/wiki"

# Logging
LOGGER_NAME = "cutevariant"
LOG_LEVEL = "DEBUG"
LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "notset": logging.NOTSET,
}

################################################################################


def logger(name=LOGGER_NAME, logfilename=None):
    """Return logger of given name, without initialize it.

    Equivalent of logging.getLogger() call.
    """
    logger = logging.getLogger(name)
    FORMAT = "%(levelname)s: [%(filename)s:%(lineno)s:%(funcName)s()] %(message)s"
    logging.basicConfig(format=FORMAT)
    return logger


_logger = logging.getLogger(LOGGER_NAME)
_logger.setLevel(LOG_LEVEL)

# log file
formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(message)s")
file_handler = RotatingFileHandler(
    DIR_LOGS
    + LOGGER_NAME
    + "_"
    + dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    + ".log",
    "a",
    100_000_000,
    1,
)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(formatter)
_logger.addHandler(file_handler)

# terminal log
# stream_handler = logging.StreamHandler()
# formatter = logging.Formatter("%(levelname)s: %(message)s")
# stream_handler.setFormatter(formatter)
# stream_handler.setLevel(LOG_LEVEL)
# _logger.addHandler(stream_handler)


def log_level(level):
    """Set terminal/file log level to given one.
    .. note:: Don't forget the propagation system of messages:
        From logger to handlers. Handlers receive log messages only if
        the main logger doesn't filter them.
    """
    # Main logger
    _logger.setLevel(level.upper())
    # Handlers
    [
        handler.setLevel(level.upper())
        for handler in _logger.handlers
        if handler.__class__
        in (logging.StreamHandler, logging.handlers.RotatingFileHandler)
    ]


def is_gz_file(filepath):
    """Return a boolean according to the compression state of the file"""
    with open(filepath, "rb") as test_f:
        return test_f.read(3) == b"\x1f\x8b\x08"


def get_uncompressed_size(filepath):
    """Get the size of the given compressed file
    This size is stored in the last 4 bytes of the file.
    """
    with open(filepath, "rb") as file_obj:
        file_obj.seek(-4, 2)
        return int.from_bytes(file_obj.read(4), byteorder="little")


def bytes_to_readable(size) -> str:
    """return human readable size from bytes
    
    Args:
        size (int): size in bytes
    
    Returns:
        str: readable size
    """
    out = ""
    for count in ["Bytes", "KB", "MB", "GB"]:
        if size > -1024.0 and size < 1024.0:
            return "%3.1f%s" % (size, count)
        size /= 1024.0
    return "%3.1f%s" % (size, "TB")


def snake_to_camel(name: str) -> str:
    """Convert snake_case name to CamelCase name

    Args:
        name (str): a snake string like : query_view

    Returns:
        str: a camel string like: QueryView
    """
    return "".join([i.capitalize() for i in name.split("_")])


def camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case name

    Args:
        name (str): a snake string like : QueryView

    Returns:
        str: a camel string like: query_view
    """
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def is_json_file(filename):

    if not os.path.exists(filename):
        return False

    with open(filename) as file:
        try:
            json.load(file)
        except Exception as e:
            return False
        finally:
            return True
