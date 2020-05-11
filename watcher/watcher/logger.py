import datetime as dt
import logging
import time
from logging.handlers import HTTPHandler
from pprint import PrettyPrinter
from threading import RLock, current_thread

import requests

from watcher import settings
from watcher.exc import WatcherLogstashError


class DSMConsoleFormatter(logging.Formatter):
    pretty_printer = PrettyPrinter(width=200, compact=True)

    def format(self, record):
        msg = super().format(record)
        if hasattr(record, 'extra') and record.extra:
            msg += f'\nLog extra:\n{self.pretty_printer.pformat(record.extra)}'
        return msg


class LogstashHandler(HTTPHandler):
    __start_tik = time.monotonic()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.http_session = requests.Session()
        self.lock = RLock()

    def mapLogRecord(self, record):
        asctime = getattr(record, 'asctime', None) or str(dt.datetime.now(dt.timezone.utc))

        log_rec_map = {
            'srv': settings.APP_NAME,
            'asctime': asctime,
            'name': record.name,
            'funcName': record.funcName,
            'levelname': record.levelname,
            'message': record.getMessage(),
            'exc_text': str(record.exc_text) if record.exc_text else None,
            'thread_name': current_thread().name,
            'uptime': int(time.monotonic() - self.__start_tik),
        }
        if hasattr(record, 'extra'):
            log_rec_map.update(record.extra)

        return log_rec_map

    def emit(self, record):
        with self.lock:
            try:
                self.http_session.post(
                    url=settings.LOGSTASH_HOST,
                    timeout=settings.HTTP_TIMEOUT,
                    json=self.mapLogRecord(record),
                    headers={'Content-type': 'application/json'}
                )
            except Exception as exc:
                raise WatcherLogstashError('the LogstashHandler could not send the request!') from exc
