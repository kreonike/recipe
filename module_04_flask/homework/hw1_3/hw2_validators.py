"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""


from typing import Optional
from wtforms import ValidationError, Field
from flask_wtf import FlaskForm


def number_length(min: int, max: int, message: Optional[str] = None):
    """
    :валидатор для проверки длины числа.
    :min: минимальная длина числа.
    :max: максимальная длина числа.
    :message: сообщение об ошибке.
    :return: функция-валидатор.
    """

    def _number_length(field: Field):
        value = field.data
        if value is None:
            raise ValidationError(message or 'Поле обязательно для заполнения.')

        # преобразуем значение в строку и проверяем длину
        value_str = str(value)
        if not (min <= len(value_str) <= max):
            raise ValidationError(message or f'Длина числа должна быть от {min} до {max} цифр')

    return _number_length


class NumberLength:
    """
    валидатор для проверки длины числа.
    """

    def __init__(self, min: int, max: int, message: Optional[str] = None):
        """
        :min: минимальная длина числа.
        :max: максимальная длина числа.
        :message: сообщение об ошибке.
        """
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        value = field.data
        if value is None:
            raise ValidationError(self.message or 'Поле обязательно для заполнения.')

        # преобразуем значение в строку и проверяем длину
        value_str = str(value)
        if not (self.min <= len(value_str) <= self.max):
            raise ValidationError(self.message or f'Длина числа должна быть от {self.min} до {self.max} цифр')
