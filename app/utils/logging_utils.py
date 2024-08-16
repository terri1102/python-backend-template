import os
import logging
from logging import Logger

from typing import Any, Optional


from app.core.config import settings


class SingletonType(type):
    __instance: Optional[Any] = None

    def __call__(cls, *args, **kwargs):  # type: ignore
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletonType, cls).__call__(*args, **kwargs)
            return cls.__instance


class AppLogger:
    __metaclass__ = SingletonType
    _logger = None

    def __init__(self) -> None:
        self._logger = logging.getLogger(settings.PROJECT_NAME)
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s - (%(filename)s:%(lineno)s) %(message)s")

        import datetime

        now = datetime.datetime.now()

        dirname = "./log"
        if not os.path.isdir(dirname):
            os.mkdir(dirname)

        file_handler = logging.FileHandler(f'{dirname}/{now.strftime("%Y-%m-%d %H:%M:%S")}.log')
        stream_handler = logging.StreamHandler()

        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        if not self._logger.hasHandlers():
            self._logger.addHandler(file_handler)
            self._logger.addHandler(stream_handler)

    def get_logger(self) -> Logger | None:
        return self._logger
