"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""


def human_readable_size(size_in_kb: float) -> str:
    """
    Преобразует размер из килобайт в человекочитаемый формат (КБ, МБ, ГБ и т.д.).
    """
    units = ['КБ', 'МБ', 'ГБ', 'ТБ']
    size = size_in_kb
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.2f} {units[unit_index]}"


def get_summary_rss(ps_output_file_path: str) -> str:
    """
    Вычисляет общий объем использования памяти RSS из файла вывода ps aux и возвращает его в человекочитаемом формате.
    """
    total_kb = 0

    with open(ps_output_file_path, 'r') as file:
        lines = file.readlines()[1:]  # Пропускаем заголовок

        for line in lines:
            columns = line.split()
            rss = int(columns[5])  # RSS в килобайтах в выводе ps aux
            total_kb += rss

    return f'Общий RSS: {human_readable_size(total_kb)}'


if __name__ == '__main__':
    path: str = 'output_file.txt'
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)
