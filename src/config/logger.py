import logging
import logging.config
import os
from src.config.correlation import correlation_id_var


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv("LOG_FORMAT", "text")
TEXT_FORMATTER = "%(asctime)s | %(levelname)s | %(name)s | %(correlation_id)s | %(message)s"
JSON_FORMATTER = '{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","correlation_id":"%(correlation_id)s","message":"%(message)s"}'


class CorrelationIdFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = correlation_id_var.get()
        return True


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
        "filters": {
            "correlation_id": {
                "()": "src.config.logger.CorrelationIdFilter"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "filters": ["correlation_id"],
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
