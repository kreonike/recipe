"""
Консольная утилита lsof (List Open Files) выводит информацию о том, какие файлы используют какие-либо процессы.
Эта команда может рассказать много интересного, так как в Unix-подобных системах всё является файлом.

Но нам пока нужна лишь одна из её возможностей.
Запуск lsof -i :port выдаст список процессов, занимающих введённый порт.
Например, lsof -i :5000.

Как мы с вами выяснили, наш сервер отказывается запускаться, если кто-то занял его порт. Напишите функцию,
которая на вход принимает порт и запускает по нему сервер. Если порт будет занят,
она должна найти процесс по этому порту, завершить его и попытаться запустить сервер ещё раз.
"""
from typing import List

from flask import Flask

import os
import subprocess
from typing import List
from flask import Flask

app = Flask(__name__)

def get_pids(port: int) -> List[int]:
    """
    Возвращает список PID процессов, использующих указанный порт.
    @param port: Номер порта.
    @return: Список PID.
    """
    if not isinstance(port, int):
        raise ValueError("Порт должен быть целым числом.")

    try:
        # Запускаем команду lsof для поиска процессов
        result = subprocess.run(['lsof', '-i', f':{port}'], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.splitlines()
        pids = []
        for line in lines[1:]:
            parts = line.split()
            if len(parts) > 1:
                pids.append(int(parts[1]))
        return pids
    except subprocess.CalledProcessError:
        return []

def free_port(port: int) -> None:
    """
    Завершает процессы, использующие указанный порт.
    @param port: Номер порта.
    """
    pids = get_pids(port)
    for pid in pids:
        try:
            os.kill(pid, 9)
        except ProcessLookupError:
            pass

def run(port: int) -> None:
    """
    Запускает Flask-приложение на указанном порту.
    Если порт занят, завершает процессы, использующие его.
    @param port: Номер порта.
    """
    free_port(port)
    app.run(port=port)

if __name__ == '__main__':
    run(5000)
