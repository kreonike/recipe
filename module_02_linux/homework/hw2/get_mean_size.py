"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys


def get_mean_size(ls_output: str) -> float:
    ...


if __name__ == '__main__':
    data: str = sys.stdin.read()
    mean_size: float = get_mean_size(data)
    print(mean_size)

    """
    Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

    $ ls -l | python3 get_mean_size.py

    Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
    а возвращает средний размер файла в каталоге.
    """

    import sys


    def get_mean_size(ls_output: str) -> float:
        lines = ls_output.strip().splitlines()

        total_size = 0
        file_count = 0

        for line in lines[1:]:
            columns = line.split()

            if len(columns) >= 7 and columns[0][0] != 'd':
                try:
                    size = int(columns[4])
                    total_size += size
                    file_count += 1
                except (ValueError, IndexError):
                    continue

        if file_count == 0:
            return 0
        return total_size / file_count


    if __name__ == '__main__':
        data: str = sys.stdin.read()
        mean_size: float = get_mean_size(data)
        print(mean_size)
