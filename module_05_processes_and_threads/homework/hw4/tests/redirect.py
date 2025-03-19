"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""

import sys
from types import TracebackType
from typing import Type, Literal, IO


class Redirect:
    def __init__(self, stdout: IO = None, stderr: IO = None) -> None:
        """
        Инициализация контекстного менеджера.
        :param stdout: IO-объект для перенаправления stdout (по умолчанию None).
        :param stderr: IO-объект для перенаправления stderr (по умолчанию None).
        """
        self.stdout = stdout
        self.stderr = stderr
        self.old_stdout = None
        self.old_stderr = None

    def __enter__(self):
        """
        Вход в контекстный менеджер. Сохраняем текущие потоки и перенаправляем их.
        """
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

        if self.stdout:
            sys.stdout = self.stdout
        if self.stderr:
            sys.stderr = self.stderr

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        """
        Выход из контекстного менеджера. Восстанавливаем оригинальные потоки.
        """
        # TODO надо записать в файл поток stderr:
        #  if self.stderr:
        #      sys.stderr.write(traceback.format_exc())
        if self.stdout:
            sys.stdout = self.old_stdout
        if self.stderr:
            sys.stderr = self.old_stderr

        if self.stdout:
            self.stdout.close()
        if self.stderr:
            self.stderr.close()

        return None
