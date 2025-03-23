import logging
import requests
import json


class JSONHTTPHandler(logging.Handler):
    """
    Обработчик, который отправляет логи в формате JSON на сервер.
    """

    def __init__(self, host, url, method="POST"):
        super().__init__()
        self.host = host
        self.url = url
        self.method = method

    def emit(self, record):
        """
        Отправляет лог на сервер в формате JSON.
        """
        try:
            log_entry = self.format(record)
            log_data = json.loads(log_entry)

            requests.post(
                f"http://{self.host}{self.url}",
                json=log_data,  # Отправляем данные в формате JSON
                headers={"Content-Type": "application/json"},
            )
        except Exception as e:
            print(f"Error sending log to server: {e}")
