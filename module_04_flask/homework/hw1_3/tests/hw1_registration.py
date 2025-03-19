"""
В эндпоинт /registration добавьте все валидаторы, о которых говорилось в последнем видео:

1) email (текст, обязательно для заполнения, валидация формата);
2) phone (число, обязательно для заполнения, длина — десять символов, только положительные числа);
3) name (текст, обязательно для заполнения);
4) address (текст, обязательно для заполнения);
5) index (только числа, обязательно для заполнения);
6) comment (текст, необязательно для заполнения).
"""

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, Email, NumberRange, Optional

app = Flask(__name__)
app.config["WTF_CSRF_ENABLED"] = False


class RegistrationForm(FlaskForm):
    # Валидация email: проверка формата email
    email = StringField(validators=[
        InputRequired(message='Поле "Email" обязательно для заполнения.'),
        Email(message='Некорректный формат email.')
    ])

    # Валидация phone: длина - 10 символов, без отрицательных чисел
    phone = IntegerField(validators=[
        InputRequired(message='Поле "Телефон" обязательно для заполнения.'),
        NumberRange(min=1000000000, max=9999999999,
                    message='Номер телефона должен состоять из 10 цифр.')
    ])

    # Валидация name: обязательно для заполнения
    name = StringField(validators=[
        InputRequired(message='Поле "Имя" обязательно для заполнения.')
    ])

    # Валидация address: обязательно для заполнения
    address = StringField(validators=[
        InputRequired(message='Поле "Адрес" обязательно для заполнения.')
    ])

    # Валидация index: только числа, обязательно для заполнения
    index = IntegerField(validators=[
        InputRequired(message='Поле "Индекс" обязательно для заполнения.')
    ])

    # Валидация comment: необязательно для заполнения
    comment = StringField(validators=[
        Optional()
    ])


@app.route('/registration', methods=['POST'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        phone = form.phone.data
        return f' зарегистрирован пользователь: {email} с номером: +7{phone}'

    # Ошибки валидации
    errors_list = form.errors
    return f'Не верный ввод, {errors_list}', 400


if __name__ == "__main__":
    app.run(debug=True)
