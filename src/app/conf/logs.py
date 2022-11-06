import logging

import structlog
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from app.conf.env_reader import env

if settings.DEBUG:
    RENDERER = structlog.dev.ConsoleRenderer()
else:
    RENDERER = structlog.processors.JSONRenderer(serializer=settings.JSON_SERIALIZER)

LOGGING_TIMESTAMP_FORMAT = env('LOGGING_TIMESTAMP_FORMAT', cast=str, default='iso')
logging_level_name = env(
    'LOGGING_LEVEL',
    cast=str,
    default="DEBUG" if settings.DEBUG else "INFO"
)
try:
    LOGGING_LEVEL = logging.getLevelNamesMapping()[logging_level_name]
except KeyError as ex:
    raise ImproperlyConfigured(
        "LOGGING_LEVEL setting should be valid python logging option. "
        f"Your value is {logging_level_name}",
    )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'structlog': {
            '()': structlog.stdlib.ProcessorFormatter,
            'processors': [
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                RENDERER,
            ],
            'foreign_pre_chain': [
                structlog.contextvars.merge_contextvars,
                structlog.stdlib.add_log_level,
                structlog.processors.TimeStamper(fmt=LOGGING_TIMESTAMP_FORMAT),
            ],
        }
    },
    'handlers': {
        'primary': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'structlog',
        },
    },
    'root': {
        'level': LOGGING_LEVEL,
        'handlers': ['primary'],
    },
    'loggers': {
        'django': {
            'handlers': ['primary'],
            'level': LOGGING_LEVEL,
            'propagate': False,
        },
        'django.request': {
            'handlers': ['primary'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt=LOGGING_TIMESTAMP_FORMAT),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.make_filtering_bound_logger(LOGGING_LEVEL),  # type: ignore
    cache_logger_on_first_use=True,
)
