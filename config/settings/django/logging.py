LOGGING = {
    "version": 1,
    "formatters": {
        "verbose": {
            "format": "{asctime} | {levelname:<7} | {module}:<{filename}>:{lineno} - {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    },
}
