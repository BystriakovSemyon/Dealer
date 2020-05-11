import logging
import logging.config
import threading
from collections import ChainMap
import watcher.settings as settings


class DSMAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        kwargs['extra'] = {'extra': ChainMap(kwargs.get('extra', {}), self.extra)}
        return msg, kwargs


class InitLogger:
    """Миксин для инициализации логера(адаптер)"""
    def __init__(self, *args, log_context=None, **kwargs):
        self.log_context = log_context if log_context else {}
        self.logger = DSMAdapter(
            logging.getLogger(f'{self.__class__.__module__}.{self.__class__.__name__}'),
            self.log_context
        )
        super().__init__(*args, **kwargs)


_init_lock = threading.Lock()
_initialized = False


def init_logging():
    """
    Инициализирует логирование, в большинстве сервисов данный метод вызывается один раз, но в некоторых несколько
    """
    global _initialized
    if not _initialized:
        with _init_lock:
            if not _initialized:
                logging.config.dictConfig(settings.LOGGING)
                _initialized = True


def setup_logger(logger_name, log_context=None):
    """Создание корневого логера сервиса."""
    init_logging()
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    app_logger = logging.getLogger(logger_name)
    app_logger.setLevel(log_level)
    return DSMAdapter(app_logger, log_context if log_context is not None else {})


def use_logs(cls):
    """Подключить использование журнала.

    Декоратор определяет переменную класса logger, куда записывает логгер для
    указанного класса.

    >>> @use_logs
    ... class A:
    ...     def f(self):
    ...         self.logger.info("hi!")
    """

    cls.logger = logging.getLogger(cls.__module__ + "." + cls.__name__)
    return cls
