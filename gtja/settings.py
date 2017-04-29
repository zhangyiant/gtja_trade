LOGGING = {
    "version": 1,
    "formatters": {
        'verbose': {
            'format': "%(levelname)s %(asctime)s %(message)s"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose"
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "verbose",
            "filename": "stock.log",
            "when": "D",
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"]
    }
}
