"""
Реализуйте endpoint, начинающийся с /max_number, в который можно передать список чисел, разделённых слешем /.
Endpoint должен вернуть текст «Максимальное переданное число {number}»,
где number — выделенное курсивом наибольшее из переданных чисел.

Примеры:

/max_number/10/2/9/1
Максимальное число: 10

/max_number/1/1/1/1/1/1/1/2
Максимальное число: 2

"""

from flask import Flask

app = Flask(__name__)


@app.route('/max_number/<path:numbers>')
def max_number(numbers: str):
    parts = numbers.split('/')
    num_list = []

    for part in parts:
        try:
            num = int(part)
        except ValueError:
            try:
                num = float(part)
            except ValueError:
                continue
        num_list.append(num)

    if not num_list:
        return 'Это не число'
    max_num = max(num_list)

    return f'Максимальное число: {max_num}'


if __name__ == '__main__':
    app.run(debug=True)
