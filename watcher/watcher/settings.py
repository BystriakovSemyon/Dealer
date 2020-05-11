import os
import sys
from urllib3.util.timeout import Timeout, _Default

from watcher.exc import NoAppNameError


DEBUG = bool(int(os.getenv('DEBUG') or 0))

APP_NAME = os.getenv('APP_NAME')
if not APP_NAME:
    raise NoAppNameError('APP_NAME is mandatory parameter!')


WORK_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_PATH = os.path.join(WORK_DIR, 'log')
LOG = os.path.join(LOG_PATH, 'log.txt')

LOGSTASH_HOST = os.getenv('LOGSTASH_HOST')

HTTP_CONNECT_TIMEOUT = os.getenv('HTTP_CONNECT_TIMEOUT')
HTTP_READ_TIMEOUT = os.getenv('HTTP_READ_TIMEOUT')
HTTP_RETRY_COUNT = int(os.getenv('HTTP_RETRY_COUNT') or 4)
HTTP_RETRY_BACKOFF = float(os.getenv('HTTP_RETRY_BACKOFF') or 15)
if HTTP_CONNECT_TIMEOUT or HTTP_READ_TIMEOUT:
    HTTP_TIMEOUT = Timeout(
        connect=int(HTTP_CONNECT_TIMEOUT or 0) or _Default,
        read=int(HTTP_READ_TIMEOUT or 0) or _Default
    )
else:
    http_timeout = int(os.getenv('HTTP_TIMEOUT') or 60)
    HTTP_TIMEOUT = Timeout(connect=http_timeout, read=http_timeout)

TIME_ZONE = 'UTC'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'class': 'watcher.logger.DSMConsoleFormatter',
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': sys.stdout
        },
        'logstash': {
            'class': 'watcher.logger.LogstashHandler',
            'url':  '',
            'host': '',
            'level': 'DEBUG'
        }
    },
    'loggers': {
        'sqlalchemy': {'level': 'INFO'},
        'sqlalchemy.engine': {'level': 'WARNING'},
        'sqlalchemy.orm': {'level': 'WARNING'},
        'pika': {'level': 'INFO'},
        'apscheduler': {'level': 'INFO'},
        'console': {'handlers': ['console'], 'level': 'INFO', 'propagate': False}
    },
    'root': {
        'handlers': ['console', 'logstash'],
        'level': 'DEBUG'
    }
}
