import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor
import time
import logging
from typing import List, Dict
from werkzeug.serving import WSGIRequestHandler


class PerformanceTester:
    def __init__(self, base_url: str = 'http://127.0.0.1:5000'):
        self.base_url = base_url
        self.session = requests.Session()
        self.setup_session()
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def setup_session(self):
        """Настройка сессии с повторным использованием соединений."""
        retry = Retry(total=3, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry, pool_connections=100, pool_maxsize=100)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def make_request(self, endpoint: str, use_session: bool) -> float:
        """Отправка одного запроса с замером времени."""
        start = time.perf_counter()
        try:
            if use_session:
                response = self.session.get(
                    f'{self.base_url}{endpoint}',
                    headers=self.headers
                )
            else:
                response = requests.get(
                    f'{self.base_url}{endpoint}',
                    headers=self.headers
                )

            # Проверяем статус ответа
            if response.status_code == 403:
                logging.error(f'403 Forbidden: {response.text}')
                return 0.0

            response.raise_for_status()
            return time.perf_counter() - start

        except requests.RequestException as e:
            logging.error(f'Request failed: {str(e)}')
            return 0.0

    def test_sequential(self, endpoint: str, num_requests: int, use_session: bool) -> float:
        """Последовательные запросы."""
        total_time = 0.0
        for _ in range(num_requests):
            total_time += self.make_request(endpoint, use_session)
        return total_time

    def test_threaded(self, endpoint: str, num_requests: int, use_session: bool, max_workers: int = 10) -> float:
        """Параллельные запросы с использованием потоков."""
        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            list(executor.map(
                lambda _: self.make_request(endpoint, use_session),
                range(num_requests)
            ))
        return time.perf_counter() - start

    def run_tests(self, endpoint: str, request_counts: List[int]) -> List[Dict]:
        """Запуск всех тестовых сценариев."""
        results = []
        for count in request_counts:
            for use_session in [True, False]:
                for use_threading in [True, False]:
                    test_name = f'{count} req | {'Session' if use_session else 'No session'} | {'Threaded' if use_threading else 'Sequential'}'
                    print(f'Running: {test_name}')

                    if use_threading:
                        duration = self.test_threaded(endpoint, count, use_session)
                    else:
                        duration = self.test_sequential(endpoint, count, use_session)

                    results.append({
                        "Requests": count,
                        "Session": "+S" if use_session else "-S",
                        "Threading": "+T" if use_threading else "-T",
                        "Time (sec)": round(duration, 4)
                    })
        return results


def configure_server():
    """Настройка сервера для поддержки keep-alive соединений."""
    WSGIRequestHandler.protocol_version = 'HTTP/1.1'
    logging.basicConfig(level=logging.DEBUG)


def generate_report():
    configure_server()

    tester = PerformanceTester()
    request_counts = [10, 100, 1000]
    endpoint = '/api/books/1'

    results = tester.run_tests(endpoint, request_counts)

    print('\n## Performance Test Results')
    print('| Requests | Session | Threading | Time (sec) |')
    print('|----------|---------|-----------|------------|')
    for result in results:
        print(f"| {result['Requests']} | {result['Session']} | {result['Threading']} | {result['Time (sec)']} |")


if __name__ == '__main__':
    generate_report()