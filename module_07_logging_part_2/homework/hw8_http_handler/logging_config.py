from json_http_handler import JSONHTTPHandler

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "{levelname:8} | {name:10} | {asctime} | {lineno:4} | {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
        "json": {
            "()": "json_log_formatter.JSONFormatter",  # Используем JSON-форматтер
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "http": {
            "level": "INFO",
            "()": JSONHTTPHandler,  # Используем наш обработчик
            "host": "127.0.0.1:3000",
            "url": "/log",
            "method": "POST",
            "formatter": "json",  # Используем JSON-форматтер
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "http"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
