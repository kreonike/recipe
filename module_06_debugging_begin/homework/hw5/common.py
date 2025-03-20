import logging

class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        msg = msg.replace('"', '\\"')
        return msg, kwargs

def configure_logging(level=logging.DEBUG):
    formatter = logging.Formatter(
        '{'
        '"time": "%(asctime)s", '
        '"level": "%(levelname)-7s", '
        '"message": "%(message)s"}',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler('measure_me.log', mode='w')
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=level,
        handlers=[file_handler]
    )