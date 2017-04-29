LOGGING = {
    "version": 1,
    "formatters": {
        'verbose': {
            'format': "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
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
            "filename": "o:/log/icbc.log",
            "when": "D",
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"]
    }
}
