import unittest
from hw1_registration import app

class TestRegistration(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_valid_registration(self):
        # Успешная регистрация с корректными данными
        data = {
            'email': 'kreonike@gmail.com',
            'phone': '7930800000',
            'name': 'Dmitry',
            'address': '3 yamskaya, 14-1',
            'index': '603167',
            'comment': 'test'
        }
        response = self.client.post('/registration', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'registered user: kreonike@gmail.com', response.data)

    def test_invalid_email(self):
        # Ошибка валидации: некорректный email
        data = {
            'email': 'invalid-email',
            'phone': '7930800000',
            'name': 'Dmitry',
            'address': '3 yamskaya, 14-1',
            'index': '603167',
            'comment': 'test'
        }
        response = self.client.post('/registration', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Некорректный формат email', response.data)

    def test_missing_phone(self):
        # Ошибка валидации: отсутствует телефон
        data = {
            'email': 'kreonike@gmail.com',
            'phone': '',
            'name': 'Dmitry',
            'address': '3 yamskaya, 14-1',
            'index': '603167',
            'comment': 'test'
        }
        response = self.client.post('/registration', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Поле "Телефон" обязательно для заполнения', response.data)

    def test_invalid_phone_length(self):
        # Ошибка валидации: неправильная длина телефона
        data = {
            'email': 'kreonike@gmail.com',
            'phone': '12345',
            'name': 'Dmitry',
            'address': '3 yamskaya, 14-1',
            'index': '603167',
            'comment': 'test'
        }
        response = self.client.post('/registration', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Номер телефона должен состоять из 10 цифр', response.data)

    def test_missing_name(self):
        # Ошибка валидации: отсутствует имя
        data = {
            'email': 'kreonike@gmail.com',
            'phone': '7930800000',
            'name': '',
            'address': '3 yamskaya, 14-1',
            'index': '603167',
            'comment': 'test'
        }
        response = self.client.post('/registration', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Поле "Имя" обязательно для заполнения', response.data)

    def test_missing_address(self):
        # Ошибка валидации: отсутствует адрес
        data = {
            'email': 'kreonike@gmail.com',
            'phone': '7930800000',
            'name': 'Dmitry',
            'address': '',
            'index': '603167',
            'comment': 'test'
        }
        response = self.client.post('/registration', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Поле "Адрес" обязательно для заполнения', response.data)

    def test_missing_index(self):
        # Ошибка валидации: отсутствует индекс
        data = {
            'email': 'kreonike@gmail.com',
            'phone': '7930800000',
            'name': 'Dmitry',
            'address': '3 yamskaya, 14-1',
            'index': '',
            'comment': 'test'
        }
        response = self.client.post('/registration', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Поле "Индекс" обязательно для заполнения', response.data)

    def test_optional_comment(self):
        # Успешная регистрация без комментария
        data = {
            'email': 'kreonike@gmail.com',
            'phone': '7930800000',
            'name': 'Dmitry',
            'address': '3 yamskaya, 14-1',
            'index': '603167',
            'comment': ''
        }
        response = self.client.post('/registration', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'registered user: kreonike@gmail.com', response.data)


if __name__ == '__main__':
    unittest.main()