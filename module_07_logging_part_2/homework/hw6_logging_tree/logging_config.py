LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "debug_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": "calc_debug.log",
            "mode": "a",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": "calc_error.log",
            "mode": "a",
        },
        "utils_file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "standard",
            "filename": "utils.log",
            "when": "H",
            "interval": 1,
            "backupCount": 10,
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "debug_file", "error_file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "utils": {
            "handlers": ["utils_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
