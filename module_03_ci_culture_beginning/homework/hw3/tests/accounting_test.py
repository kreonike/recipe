import unittest
from accounting import app, storage


class TestAccountingApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

        storage.clear()

        #  изначальные данные
        cls.app.get('/add/20250101/100')
        cls.app.get('/add/20250203/3000')
        cls.app.get('/add/20250318/5500')

    def test_add_expense_valid_date(self):
        # валидная дата
        response = self.app.get('/add/20250318/100')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Трата 100 р. за 18.03.2025 добавлена.')

    def test_add_expense_invalid_date(self):
        # Проверка неправильный месяц
        response = self.app.get('/add/20251318/200')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Ошибка: некорректный формат данных', response.data.decode('utf-8'))

    def test_calculate_year(self):
        #  расчет за год
        response = self.app.get('/calculate/2025')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Траты за 2025 год: 8600 р.')

    def test_calculate_year_empty(self):
        # нет данных
        response = self.app.get('/calculate/2024')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Траты за 2024 год: 0 р.')

    def test_calculate_month(self):
        # Проверка за месяц
        response = self.app.get('/calculate/2025/01')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Суммарные траты за 01.2025: 100 р.')

    def test_calculate_month_empty(self):
        # нет данных
        response = self.app.get('/calculate/2024/04')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Суммарные траты за 04.2024: 0 р.')

    def test_calculate_month_invalid(self):
        # неправильный месяц
        response = self.app.get('/calculate/2025/13')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Ошибка: месяц должен быть от 1 до 12', response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
