"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""

from flask import Flask
import subprocess

app = Flask(__name__)


@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    # uptime
    result = subprocess.run(['uptime'], stdout=subprocess.PIPE, text=True)
    uptime_output = result.stdout.strip()

    return f'Current uptime is {uptime_output}'


if __name__ == '__main__':
    app.run(debug=True)
