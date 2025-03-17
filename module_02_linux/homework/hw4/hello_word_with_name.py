"""
Реализуйте endpoint /hello-world/<имя>, который возвращает строку «Привет, <имя>. Хорошей пятницы!».
Вместо хорошей пятницы endpoint должен уметь желать хорошего дня недели в целом, на русском языке.

Пример запроса, сделанного в субботу:

/hello-world/Саша  →  Привет, Саша. Хорошей субботы!
"""

from flask import Flask
from datetime import datetime

app = Flask(__name__)

weekdays_ru = ("понедельника", "вторника", "среды", "четверга", "пятницы", "субботы", "воскресенья")


@app.route('/hello-world/<name>')
def hello_world(name: str):
    current_weekday = datetime.today().weekday()
    weekday_ru = weekdays_ru[current_weekday]

    return f"Привет, {name}. Хорошего {weekday_ru}!"


if __name__ == '__main__':
    app.run(debug=True)
