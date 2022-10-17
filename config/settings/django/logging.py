"""
Django uses and extends Python’s builtin logging module to perform system logging. This
module is discussed in detail in Python’s own documentation; this section provides a
quick overview.

* https://docs.djangoproject.com/en/4.1/topics/logging/
"""
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
