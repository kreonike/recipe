import logging
import sys
import json
from logging import Handler


class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        msg = json.dumps(msg, ensure_ascii=False)
        return msg, kwargs


class LevelBasedFileHandler(Handler):
    """
    Пользовательский хендлер для записи сообщений разных уровней в соответствующие файлы.
    Имя файла формируется динамически: <base_name>_<level>.log
    """

    def __init__(self, base_name):
        super().__init__()
        self.base_name = base_name

    def emit(self, record):
        level = record.levelname.lower()
        filename = f"{self.base_name}_{level}.log"

        with open(filename, "a") as f:
            f.write(self.format(record) + "\n")


def configure_logging(level=logging.INFO):
    formatter = logging.Formatter(
        "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    level_file_handler = LevelBasedFileHandler(base_name="calc")
    level_file_handler.setFormatter(formatter)

    logging.basicConfig(level=level, handlers=[console_handler, level_file_handler])
