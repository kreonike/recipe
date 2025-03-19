"""
Реализуйте приложение для учёта финансов, умеющее запоминать, сколько денег было потрачено за день,
а также показывать затраты за отдельный месяц и за целый год.

В программе должно быть три endpoints:

/add/<date>/<int:number> — сохранение информации о совершённой в рублях трате за какой-то день;
/calculate/<int:year> — получение суммарных трат за указанный год;
/calculate/<int:year>/<int:month> — получение суммарных трат за указанные год и месяц.

Дата для /add/ передаётся в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12), DD — число (от 01 до 31).
Гарантируется, что переданная дата имеет такой формат и она корректна (никаких 31 февраля).
"""

from flask import Flask
from datetime import datetime

app = Flask(__name__)

storage = {}


@app.route('/add/<date>/<int:number>')
def add_expense(date: str, number: int):
    try:
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:8])
        datetime(year, month, day)

        if year not in storage:
            storage[year] = {'months': {}, 'total': 0}

        storage[year]['months'].setdefault(month, 0)
        storage[year]['months'][month] += number
        storage[year]['total'] += number

        return f'Трата {number} р. за {day}.{month}.{year} добавлена.'
    except ValueError:
        return 'Ошибка: некорректная дата или формат данных', 400


@app.route('/calculate/<int:year>')
def calculate_year(year: int):
    total = storage.get(year, {}).get('total', 0)
    return f'Траты за {year} год: {total} р.'


@app.route('/calculate/<int:year>/<int:month>')
def calculate_month(year: int, month: int):
    if month < 1 or month > 12:
        return 'Ошибка: месяц должен быть от 1 до 12', 400
    total = storage.get(year, {}).get('months', {}).get(month, 0)
    return f'Суммарные траты за {month}.{year}: {total} р.'


if __name__ == '__main__':
    app.run(debug=True)
