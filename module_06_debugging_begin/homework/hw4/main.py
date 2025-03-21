"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""
"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""


from typing import Dict
import subprocess

def run_grep_command(pattern: str) -> int:
    """
    Выполняет команду grep -c и возвращает количество совпадений.
    @param pattern: шаблон для поиска
    @return: количество совпадений
    """
    result = subprocess.run(['grep', '-c', pattern, 'skillbox_json_messages.log'], capture_output=True, text=True)
    return int(result.stdout.strip())

def task1() -> Dict[str, int]:
    """
    1. Сколько было сообщений каждого уровня за сутки.
    @return: словарь вида {уровень: количество}
    """
    levels = ['INFO', 'ERROR', 'DEBUG', 'WARNING', 'CRITICAL']
    return {level: run_grep_command(f'"level": "{level}"') for level in levels}

def task2() -> int:
    """
    2. В какой час было больше всего логов.
    @return: час
    """
    # Используем awk для извлечения часа и подсчета
    result = subprocess.run(
        "awk -F'\"' '{print $4}' skillbox_json_messages.log | cut -d' ' -f2 | cut -d':' -f1 | sort | uniq -c | sort -nr | head -n 1 | awk '{print $2}'",
        shell=True, capture_output=True, text=True
    )
    return int(result.stdout.strip())

def task3() -> int:
    """
    3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
    @return: количество логов
    """
    result = subprocess.run(
        "grep '\"level\": \"CRITICAL\"' skillbox_json_messages.log | grep '\"time\": \"2025-03-20 05:' | grep -E '05:0[0-9]:|05:1[0-9]:|05:20:' | wc -l",
        shell=True, capture_output=True, text=True
    )
    return int(result.stdout.strip())

def task4() -> int:
    """
    4. Сколько сообщений содержат слово dog.
    @return: количество сообщений
    """
    return run_grep_command('dog')

def task5() -> str:
    """
    5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
    @return: слово
    """
    result = subprocess.run(
        "grep '\"level\": \"WARNING\"' skillbox_json_messages.log | awk -F'\"message\": \"' '{print $2}' | awk -F'\"' '{print $1}' | tr ' ' '\n' | sort | uniq -c | sort -nr | head -n 1 | awk '{print $2}'",
        shell=True, capture_output=True, text=True
    )
    return result.stdout.strip()

if __name__ == '__main__':
    tasks = (task1, task2, task3, task4, task5)
    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f'{i}. {task_answer}')
