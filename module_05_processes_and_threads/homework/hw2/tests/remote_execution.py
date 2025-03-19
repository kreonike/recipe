"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""

from flask import Flask, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators
import subprocess
import os
import signal

app = Flask(__name__)
app.config['SECRET_KEY'] = '*1A#@2s9s%G9cc&7H&'


class CodeForm(FlaskForm):
    code = StringField('Code', validators=[validators.InputRequired()])
    timeout = IntegerField('Timeout', validators=[validators.NumberRange(min=1, max=30)])


def run_python_code_in_subprocess(code: str, timeout: int):
    try:
        # Запускаем процесс с использованием prlimit для ограничения ресурсов
        process = subprocess.Popen(
            ['prlimit', '--nproc=1:1', 'python', '-c', code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        try:
            # Ожидаем завершения процесса с тайм-аутом
            stdout, stderr = process.communicate(timeout=timeout)
            return stdout, stderr, process.returncode
        except subprocess.TimeoutExpired:
            # Если время истекло, завершаем процесс и читаем вывод
            os.kill(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()  # Читаем оставшийся вывод
            return None, "Execution timed out", -1
    except Exception as e:
        return None, str(e), -1


@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm(request.form)
    if not form.validate():
        return jsonify({"error": "Invalid input"}), 400

    code = form.code.data
    timeout = form.timeout.data

    stdout, stderr, returncode = run_python_code_in_subprocess(code, timeout)

    if returncode == -1:
        return jsonify({"error": stderr}), 500
    elif returncode != 0:
        return jsonify({"error": stderr}), 400
    else:
        return jsonify({"output": stdout}), 200


if __name__ == '__main__':
    app.run(debug=True)