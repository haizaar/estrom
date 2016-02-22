
import logging
from logging.config import dictConfig


def setup(conf):
    dictConfig(conf)


class LoggerMixIn:
    def __init__(self, *args, **kwargs):
        logger_name = getattr(self, "__logger_name__", self.__class__.__name__)
        self.logger = logging.getLogger(logger_name)

        for lvl in ["CRITICAL", "DEBUG", "INFO", "WARN", "WARNING", "ERROR", "FATAL"]:
            setattr(self.logger, lvl, getattr(logging, lvl))

        super().__init__(*args, **kwargs)

