import logging
import json


class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        # Сериализуем сообщение в JSON-формат с поддержкой нелатинских символов
        msg = json.dumps(msg, ensure_ascii=False)
        return msg, kwargs


def configure_logging(level=logging.INFO):
    formatter = logging.Formatter('{'
                                  '"time": "%(asctime)s", '
                                  '"level": "%(levelname)-7s", '
                                  '"message": "%(message)s"}',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    file_handler = logging.FileHandler('skillbox_json_messages.log', mode='w')
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=level,
        handlers=[file_handler]
    )