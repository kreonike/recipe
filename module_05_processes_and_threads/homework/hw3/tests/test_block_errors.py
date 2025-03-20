import unittest
from block_errors import BlockErrors


class TestBlockErrors(unittest.TestCase):
    def test_ignore_expected_exception(self):
        """
        Тест: игнорирование ожидаемого исключения (ZeroDivisionError).
        """
        with BlockErrors({ZeroDivisionError}):
            a = 1 / 0
        self.assertTrue(True)

    def test_propagate_unexpected_exception(self):
        """
        Тест: прокидывание неожидаемого исключения (TypeError).
        """
        with self.assertRaises(TypeError):
            with BlockErrors({ZeroDivisionError}):
                a = 1 / '0'

    def test_nested_blocks(self):
        """
        Тест: вложенные блоки с разными типами исключений.
        """
        with BlockErrors({TypeError}):
            with BlockErrors({ZeroDivisionError}):
                a = 1 / '0'  # Вызовет TypeError, который будет проигнорирован внешним блоком
            self.assertTrue(True, 'Внутренний блок: выполнено без ошибок')
        self.assertTrue(True, 'Внешний блок: выполнено без ошибок')

    def test_ignore_all_exceptions(self):
        """
        Тест: игнорирование всех исключений (Exception).
        """
        with BlockErrors({Exception}):
            a = 1 / '0'
        self.assertTrue(True, 'Выполнено без ошибок')

    def test_no_exception(self):
        """
        Тест: блок без исключений.
        """
        try:
            with BlockErrors({ZeroDivisionError}):
                a = 1 / 1
        except:
            self.fail('Исключение не должно было возникнуть')


if __name__ == '__main__':
    unittest.main()
