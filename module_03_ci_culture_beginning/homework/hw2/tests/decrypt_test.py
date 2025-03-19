import unittest
from decrypt import decrypt


class TestDecrypt(unittest.TestCase):
    def test_no_dots(self):
        self.assertEqual(decrypt('абра-кадабра'), 'абра-кадабра')

    def test_single_dot(self):
        self.assertEqual(decrypt('абраа.-кадабра'), 'абраа-кадабра')

    def test_two_dots(self):
        # Список тестовых случаев для двух точек
        test_cases = [
            ('абраа..-кадабра', 'абра-кадабра'),
            ('абраа..-.кадабра', 'абра-кадабра'),
            ('абра--..кадабра', 'абра-кадабра'),
        ]

        # Проверка всех тестовых случаев в цикле с использованием subTest
        for input_str, expected_output in test_cases:
            with self.subTest(input_str=input_str, expected_output=expected_output):
                self.assertEqual(decrypt(input_str), expected_output)

    def test_three_dots(self):
        self.assertEqual(decrypt('абрау...-кадабра'), 'абра-кадабра')

    def test_multiple_dots(self):
        # Список тестовых случаев для множества точек
        test_cases = [
            ('абра........', ''),
            ('абр......a.', 'a'),
            ('1..2.3', '23'),
            ('.', ''),
            ('1.......................', ''),
        ]

        # Проверка всех тестовых случаев в цикле с использованием subTest
        for input_str, expected_output in test_cases:
            with self.subTest(input_str=input_str, expected_output=expected_output):
                self.assertEqual(decrypt(input_str), expected_output)


if __name__ == '__main__':
    unittest.main()