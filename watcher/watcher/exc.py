class WatcherError(Exception):
    """Корневое исключение Watcher backend."""


class WatcherValidationError(WatcherError):
    """
    Исключение несоответствия данных и нашей модели.

    Рэйзить при непрохождении данными валидации.
    """


class WatcherLogstashError(WatcherError):
    """Исключение для обработки ошибок от API Logstash."""


class WatcherRabbitMQError(WatcherError):
    """Исключение для обработки ошибок от очереди сообщений RabbitMQ."""


class NoAppNameError(WatcherError):
    """Ошибка отсутствия имени у приложения."""
