import logging
import sys


class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        # TODO в прошлом модуле подсказывал, что надо для начала сериализовать msg с помощью
        #  json.dumps(msg, ensure_ascii=False)
        msg = msg.replace('"', '\\"')
        return msg, kwargs

# TODO По заданию надо разработать на базе класса Handler хендлер файлов для записи сообщний разных уровней в
#  соответствующие файлы, а так как уровней сообщений достаточно много, поэтому, чтобы не дублировать код, имя файла
#  лога удобно формировать динамически с учетом "уровня" записи:
#  "<base_name>_<level>.log"
#  где base_name передается через параметр при создании вашего хенлера, а уровень можно получить из объекта записи:
#  level = record.levelname.lower()

def configure_logging(level=logging.INFO):
    formatter = logging.Formatter(
        '%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    debug_file_handler = logging.FileHandler('calc_debug.log')
    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)

    error_file_handler = logging.FileHandler('calc_error.log')
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=level,
        handlers=[console_handler, debug_file_handler, error_file_handler]
    )
