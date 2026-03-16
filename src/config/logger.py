import logging
import logging.config
import os


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv("LOG_FORMAT", "text")
TEXT_FORMATTER = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
JSON_FORMATTER = '{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}'


def setup_logging():
    formatter = JSON_FORMATTER if LOG_FORMAT == "json" else TEXT_FORMATTER

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": formatter,
            }
    },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout"
            }
        },
        "root": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
        },
        "loggers": {
            "uvicorn": {"propagate": True},
            "uvicorn.error": {"propagate": True},
            "uvicorn.access": {"propagate": True},
        }
    })
