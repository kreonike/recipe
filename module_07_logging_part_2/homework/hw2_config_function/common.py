import logging
import sys


class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        msg = msg.replace('"', '\\"')
        return msg, kwargs


def configure_logging(level=logging.INFO):
    formatter = logging.Formatter(
        '%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logging.basicConfig(
        level=level,
        handlers=[console_handler]
    )
