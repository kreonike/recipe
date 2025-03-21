"""
У нас есть кнопочный телефон (например, знаменитая Nokia 3310), и мы хотим,
чтобы пользователь мог проще отправлять СМС. Реализуем своего собственного клавиатурного помощника.

Каждой цифре телефона соответствует набор букв:
* 2 — a, b, c;
* 3 — d, e, f;
* 4 — g, h, i;
* 5 — j, k, l;
* 6 — m, n, o;
* 7 — p, q, r, s;
* 8 — t, u, v;
* 9 — w, x, y, z.

Пользователь нажимает на клавиши, например 22736368, после чего на экране печатается basement.

Напишите функцию my_t9, которая принимает на вход строку, состоящую из цифр 2–9,
и возвращает список слов английского языка, которые можно получить из этой последовательности цифр.
"""
from typing import List
import re

# Сопоставление цифр и букв
digit_to_letters = {
    '2': '[abc]',
    '3': '[def]',
    '4': '[ghi]',
    '5': '[jkl]',
    '6': '[mno]',
    '7': '[pqrs]',
    '8': '[tuv]',
    '9': '[wxyz]'
}

def my_t9(input_numbers: str) -> List[str]:
    # Загружаем список английских слов
    with open('words', 'r') as file:
        english_words = [word.strip().lower() for word in file.readlines()]

    # Строим регулярное выражение на основе введённой последовательности цифр
    regex_pattern = ''.join(digit_to_letters[digit] for digit in input_numbers)
    regex = re.compile(f'^{regex_pattern}$')

    # Ищем слова, соответствующие регулярному выражению
    valid_words = [word for word in english_words if regex.match(word)]

    return valid_words

if __name__ == '__main__':
    numbers: str = input('Введите последовательность цифр (2-9): ')
    words: List[str] = my_t9(numbers)
    print(*words, sep='\n')