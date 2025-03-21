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

# Сопоставление цифр и букв
digit_to_letters = {
    '2': ['a', 'b', 'c'],
    '3': ['d', 'e', 'f'],
    '4': ['g', 'h', 'i'],
    '5': ['j', 'k', 'l'],
    '6': ['m', 'n', 'o'],
    '7': ['p', 'q', 'r', 's'],
    '8': ['t', 'u', 'v'],
    '9': ['w', 'x', 'y', 'z']
}

def my_t9(input_numbers: str) -> List[str]:
    with open('words', 'r') as file:
        english_words = set(word.strip().lower() for word in file.readlines())

    def generate_combinations(digits, current_combination, index):
        if index == len(digits):
            combinations.append(current_combination)
            return
        for letter in digit_to_letters[digits[index]]:
            generate_combinations(digits, current_combination + letter, index + 1)

    combinations = []
    generate_combinations(input_numbers, "", 0)

    valid_words = [word for word in combinations if word in english_words]

    return valid_words

if __name__ == '__main__':
    numbers: str = input('Введите последовательность цифр (2-9): ')
    words: List[str] = my_t9(numbers)
    print(*words, sep='\n')
