import logging.config
from logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("logger")

logger.info("info log message.")
logger.error("error log message.")
