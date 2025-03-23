import logging
import logging.config
from logging_config import LOGGING_CONFIG


class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        msg = msg.replace('"', '\\"')
        return msg, kwargs


def configure_logging(level=logging.INFO):
    logging.config.dictConfig(LOGGING_CONFIG)

    logging.getLogger().setLevel(level)
