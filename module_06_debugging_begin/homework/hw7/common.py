import logging


class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        msg = msg.replace('"', '\\"')
        return msg, kwargs

def configure_logging(level=logging.INFO):
    formatter = logging.Formatter('{'
                                  '"time": "%(asctime)s", '
                                  '"level": "%(levelname)-7s", '
                                  '"message": "%(message)s"}',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logging.basicConfig(
        level=level,
        handlers=[console_handler]
    )