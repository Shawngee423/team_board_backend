import logging
import logging.config
from pathlib import Path

from app.config.config import settings


def setup_logging(
        log_dir: str = "logs",
        log_file: str = "app.log",
        json_logs: bool = False
):
    """配置全局日志"""
    log_dir_path = Path(log_dir)
    log_dir_path.mkdir(exist_ok=True)
    log_file_path = log_dir_path / log_file

    if json_logs:
        # JSON格式日志配置
        LOGGING_CONFIG = {
            "version": 1,
            "disable_existing_loggers": False,
        "filters": {
            "ignore_watchfiles": {
                "()": "logging.Filter",
                "name": "watchfiles"
            }
        },
            "formatters": {
                "json": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "format": "%(asctime)s %(name)s %(levelname)s %(message)s"
                }
            },
            "handlers": {
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": log_file_path,
                    "formatter": "json",
                    "maxBytes": 10485760,  # 10MB
                    "backupCount": 5,
                    "filters": ["ignore_watchfiles"]
                },
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "json"
                }
            },
            "root": {
                "handlers": ["file", "console"],
                "level": settings.log_level
            }
        }
    else:
        # 普通文本日志配置
        LOGGING_CONFIG = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": settings.log_format
                }
            },
            "handlers": {
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": log_file_path,
                    "formatter": "standard",
                    "maxBytes": 10485760,  # 10MB
                    "backupCount": 5
                },
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard"
                }
            },
            "root": {
                "handlers": ["file", "console"],
                "level": settings.log_level
            }
        }

    logging.config.dictConfig(LOGGING_CONFIG)