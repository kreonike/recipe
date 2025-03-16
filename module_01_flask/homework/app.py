import datetime
from flask import Flask
from random import choice
import os
import re

app = Flask(__name__)

cars_list = ['Chevrolet', 'Renault', 'Ford', 'Lada']
cats_list = ['корниш-рекс', 'русская', 'голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']
# TODO сделайте эти переменные константами (имя констант пишется прописными буквами

counter = 0  # TODO глобальная переменная - это основной код программы должен располагаться после определения всех функций

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

with open(BOOK_FILE, 'r', encoding='utf-8') as book:  # TODO это тоже основной код программы
    text = book.read()
    words = re.findall(r'\b\w+\b', text)

@app.route('/hello_world')
def hello_function():
    return 'Привет, мир!'


@app.route('/cars')
def cars_function():
    return cars_list


@app.route('/cats')
def cats_function():
    random_cats = choice(cats_list)
    return random_cats


@app.route('/get_time/now')
def time_now_function():
    now = datetime.datetime.now()
    return f'Сейчас:: {now}'


@app.route('/get_time/future')
def time_future_function():
    future_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    return f'Время через час: {future_time}'


@app.route('/get_random_word')
def random_word_function():
    random_word = choice(words)
    return f'Рандомное слово из файла: {random_word}'


@app.route('/counter')
def counter_function():
    global counter
    counter += 1
    return f'Страница была открыта: {counter} раз(а)'


if __name__ == '__main__':
    app.run(debug=True)
