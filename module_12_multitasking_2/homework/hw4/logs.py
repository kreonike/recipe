import threading
import time

import requests


def worker():
    start_time = time.time()
    while time.time() - start_time < 20:  # Работаем 20 секунд
        current_timestamp = time.time()

        try:
            response = requests.get(
                f'http://127.0.0.1:8080/timestamp/{int(current_timestamp)}'
            )
            date_str = response.text.strip()
        except requests.exceptions.RequestException:
            date_str = 'Error getting date'

        log_entry = f'{current_timestamp} {date_str}\n'

        with threading.Lock(), open('thread_logs.txt', 'a') as k:
            k.write(log_entry)

        time.sleep(1)
# TODO Сейчас записи пишут в лог (в файл) каждый раз при поступлении новой записи, а это противоречит заданию.
#  Воркер пусть складывает всё в очередь (это специальный объект класса Queue из библиотеки multiproceccing). После
#  завершения работы всех воркеров надо ОДИН раз записать всё, что накоплено в очереди в файл лога.

def run_server():
    import subprocess

    subprocess.Popen(['python', 'server.py'])


if __name__ == '__main__':
    open('thread_logs.txt', 'w').close()

    run_server()
    time.sleep(1)

    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
        time.sleep(1)

    for t in threads:
        t.join()

    with open('thread_logs.txt', 'r') as f:
        lines = f.readlines()

    sorted_lines = sorted(lines, key=lambda x: float(x.split()[0]))

    with open('thread_logs_sorted.txt', 'w') as f:
        f.writelines(sorted_lines)

    print(
        'Программа завершена. Отсортированные логи сохранены в thread_logs_sorted.txt'
    )
