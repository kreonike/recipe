"""
Реализуйте контекстный менеджер, который будет игнорировать переданные типы исключений, возникающие внутри блока with.
Если выкидывается неожидаемый тип исключения, то он прокидывается выше.
"""

from typing import Collection, Type, Literal
from types import TracebackType


class BlockErrors:
    def __init__(self, errors: Collection) -> None:
        """
        Инициализация контекстного менеджера.
        :param errors: Коллекция типов исключений, которые нужно игнорировать.
        """
        self.errors = errors

    def __enter__(self) -> None:
        """
        Вход в контекстный менеджер.
        """
        pass

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        """
        Выход из контекстного менеджера.
        :param exc_type: Тип исключения.
        :param exc_val: Экземпляр исключения.
        :param exc_tb: Трассировка стека.
        :return: Возвращает True, если исключение нужно игнорировать, иначе None.
        """
        if exc_type is not None and issubclass(exc_type, tuple(self.errors)):
            return True
        return None
