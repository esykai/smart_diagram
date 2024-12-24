import logging

from logging import Logger, StreamHandler
from colorlog import ColoredFormatter


LOG_FORMAT: str = '%(log_color)s[%(asctime)s]: %(message)s'
DATE_FORMAT: str = '%Y-%m-%d %H:%M:%S'


def setup_logging() -> None:
    """Настройка логирования для приложения."""
    formatter: ColoredFormatter = ColoredFormatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # Настройка логирования для uvicorn
    uvicorn_logger: Logger = logging.getLogger("uvicorn")
    for handler in uvicorn_logger.handlers:  # type: ignore[attr-defined]
        handler.setFormatter(formatter)

    # Общая настройка для корневого логгера
    root_logger: Logger = logging.getLogger()
    console_handler: StreamHandler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
