import threading
import time
from multiprocessing import Queue

import requests

# Создаем очередь для хранения логов
log_queue = Queue()


def worker(worker_id):
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

        # Добавляем запись в очередь вместо записи в файл
        log_queue.put(log_entry)

        time.sleep(1)


def run_server():
    import subprocess

    subprocess.Popen(['python', 'server.py'])


if __name__ == '__main__':
    # Очищаем файл логов
    open('thread_logs.txt', 'w').close()

    run_server()
    time.sleep(1)

    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
        time.sleep(1)

    # Ждем завершения всех потоков
    for t in threads:
        t.join()

    # После завершения всех воркеров записываем все записи из очереди в файл
    with open('thread_logs.txt', 'a') as f:
        while not log_queue.empty():
            f.write(log_queue.get())

    # Сортируем записи
    with open('thread_logs.txt', 'r') as f:
        lines = f.readlines()

    sorted_lines = sorted(lines, key=lambda x: float(x.split()[0]))

    with open('thread_logs_sorted.txt', 'w') as f:
        f.writelines(sorted_lines)

    print(
        'Программа завершена. Отсортированные логи сохранены в thread_logs_sorted.txt'
    )
