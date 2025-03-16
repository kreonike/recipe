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

app = Flask(__name__)

storage = {}


@app.route('/add/<date>/<int:number>')
def add_expense(date: str, number: int):
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:8])

    storage.setdefault(year, {}).setdefault(month, 0)
    storage[year][month] += number

    return f' Трата {number} р. за {day}.{month}.{year} добавлена.'


@app.route('/calculate/<int:year>')
def calculate_year(year: int):
    total = sum(storage.get(year, {}).values())
    return f' Траты за {year} год: {total} р.'


@app.route('/calculate/<int:year>/<int:month>')
def calculate_month(year: int, month: int):
    # Получаем суммарные траты за указанный месяц
    total = storage.get(year, {}).get(month, 0)
    return f' Суммарные траты за {month}.{year}: {total} р.'


if __name__ == '__main__':
    app.run(debug=True)
