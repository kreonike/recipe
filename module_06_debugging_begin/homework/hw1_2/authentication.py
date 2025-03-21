import getpass
import hashlib
import logging
from common import configure_logging
from bisect import bisect_left

logger = logging.getLogger("password_checker")

def load_words_from_file(filename: str) -> list:
    """
    Загружает слова из файла, приводит их к нижнему регистру и сортирует.
    :param filename: Имя файла со словами.
    :return: Отсортированный список слов в нижнем регистре.
    """
    try:
        with open(filename, 'r') as file:
            words = [line.strip().lower() for line in file]
        words.sort()  # Сортируем слова для бинарного поиска
        return words
    except FileNotFoundError:
        logger.error(f"Файл {filename} не найден.")
        return []

def binary_search(word: str, sorted_words: list) -> bool:
    """
    Выполняет бинарный поиск слова в отсортированном списке.
    :param word: Слово для поиска.
    :param sorted_words: Отсортированный список слов.
    :return: True, если слово найдено, иначе False.
    """
    index = bisect_left(sorted_words, word)
    return index < len(sorted_words) and sorted_words[index] == word

def is_strong_password(password: str) -> bool:
    """
    Проверяет, является ли пароль сильным.
    Пароль считается сильным, если он не содержит слов из файла words.
    :param password: Пароль для проверки.
    :return: True, если пароль сильный, иначе False.
    """

    words = load_words_from_file('words')
    password_lower = password.lower()
    password_words = password_lower.split()
    

    for word in password_words:
        if binary_search(word, words):
            logger.warning(f'Пароль содержит запрещённое слово: {word}')
            return False
    # TODO можно уменьшить количество итераций, если регэкспами найти все "слова" в пароле (по факту, все комбинации
    #  подстрок из букв) и проверить их вхождение в words

    return True

def input_and_check_password() -> bool:
    logger.debug('Начало input_and_check_password')
    password: str = getpass.getpass()

    if not password:
        logger.warning('Вы ввели пустой пароль.')
        return False
    elif not is_strong_password(password):
        logger.warning('Вы ввели слишком слабый пароль')
        return False

    try:
        hasher = hashlib.md5()

        hasher.update(password.encode('latin-1'))

        if hasher.hexdigest() == '098f6bcd4621d373cade4e832627b4f6':
            return True
    except ValueError as ex:
        logger.exception('Вы ввели некорректный символ ', exc_info=ex)

    return False

if __name__ == '__main__':
    configure_logging(level=logging.INFO)
    logger.info('Вы пытаетесь аутентифицироваться в Skillbox')
    count_number: int = 3
    logger.info(f'У вас есть {count_number} попыток')

    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1

    logger.error('Пользователь трижды ввёл неправильный пароль!')
    exit(1)