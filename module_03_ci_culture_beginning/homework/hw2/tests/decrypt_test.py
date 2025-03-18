import unittest
from decrypt import decrypt


class TestDecrypt(unittest.TestCase):
    def test_no_dots(self):
        self.assertEqual(decrypt('абра-кадабра'), 'абра-кадабра')

    def test_single_dot(self):
        self.assertEqual(decrypt('абраа.-кадабра'), 'абраа-кадабра')

    def test_two_dots(self):
        with self.subTest():
            # TODO тут в цикле выполните проверку всех нужных вариантов
            #  https://pythobyte.com/unittest-60245/
            # https://copython.ru/kontekstnyy-menedzher-subtest-unittest-v-python
            # А также документация: https://docs.python.org/3/library/unittest.html#distinguishing-test-iterations-using-subtests
            self.assertEqual(decrypt('абраа..-кадабра'), 'абра-кадабра')
        with self.subTest():
            self.assertEqual(decrypt('абраа..-.кадабра'), 'абра-кадабра')
        with self.subTest():
            self.assertEqual(decrypt('абра--..кадабра'), 'абра-кадабра')

    def test_three_dots(self):
        self.assertEqual(decrypt('абрау...-кадабра'), 'абра-кадабра')

    def test_multiple_dots(self):
        with self.subTest():
            self.assertEqual(decrypt('абра........'), '')
        with self.subTest():
            self.assertEqual(decrypt('абр......a.'), 'a')
        with self.subTest():
            self.assertEqual(decrypt('1..2.3'), '23')
        with self.subTest():
            self.assertEqual(decrypt('.'), '')
        with self.subTest():
            self.assertEqual(decrypt('1.......................'), '')


if __name__ == '__main__':
    unittest.main()
