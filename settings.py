
from estrom.utils import DotDict

settings = DotDict({
    "crossbar": {
        "host": "localhost",
        "port": 7000,
        "realm": "estrom",
        "ns": "com.estrom",
        "notify_ns": "com.estrom.notify",
        "api_ns": "com.estrom.api",
        "debug": True,
    },

    "es": {
        "host": "localhost",
        "port": 9200,
        "percolator_type": ".percolator",
    },

    "beater": {
        "host": "localhost",
        "port": 8080,
    },

    "logging": {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s.%(msecs)03d: %(name)s %(funcName)s:%(lineno)d %(levelname)s ## %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
        "loggers": {},
    },
})
