import pytest
from freezegun import freeze_time
from hello_word_with_day import app, GREETINGS


@pytest.fixture
def client():
    app.config['debug'] = True
    with app.test_client() as client:
        yield client


def test_correct_weekday(client):
    for weekday in range(7):
        with freeze_time(f'2025-03-{18 + weekday}'):
        # TODO добавьте в контекстный менеджер и self.subTest тогда при первом неверном assert тест не завершится,
        #  а выполнятся все "кейсы" и будет отчёт для каких значений тесты провалились, а для каких были успешны)
            response = client.get('/hello-world/TestUser')
            expected_greeting = GREETINGS[weekday]
            assert expected_greeting in response.data.decode('utf-8')


def test_username_with_greeting(client):
    with freeze_time('2025-03-18'):
        response = client.get('/hello-world/Хорошей среды')
        assert 'Хорошего понедельника' in response.data.decode('utf-8')
