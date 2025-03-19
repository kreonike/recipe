"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""

from flask import Flask, request
import subprocess
import shlex

app = Flask(__name__)


@app.route('/ps', methods=['GET'])
def ps() -> str:
    # Получаем аргументы из запроса в виде списка
    args: list[str] = request.args.getlist('arg')

    # обрабатываем аргументы с помощью shlex.quote
    safe_args = [shlex.quote(arg) for arg in args]

    # Формируем команду ps с аргументами
    command = ['ps'] + safe_args

    # Выполняем команду и захватываем вывод
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

    # Возвращаем результат, обернутый в тег <pre> для форматирования
    return f'<pre>{result.stdout}</pre>'


if __name__ == '__main__':
    app.run(debug=True)
