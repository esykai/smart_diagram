import logging

from logging import Logger, StreamHandler
from colorlog import ColoredFormatter


LOG_FORMAT: str = '%(log_color)s[%(asctime)s]: %(message)s'
DATE_FORMAT: str = '%Y-%m-%d %H:%M:%S'


def setup_logging() -> None:
    """Настройка логирования для приложения."""
    log_colors = {
        'DEBUG': 'bold_blue',
        'INFO': 'blue',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    formatter: ColoredFormatter = ColoredFormatter(
        LOG_FORMAT, datefmt=DATE_FORMAT, log_colors=log_colors
    )

    # Настройка логирования для aiogram
    aiogram_logger: Logger = logging.getLogger('aiogram')
    for handler in aiogram_logger.handlers:  # type: ignore[attr-defined]
        handler.setFormatter(formatter)

    # Общая настройка для корневого логгера
    root_logger: Logger = logging.getLogger()
    console_handler: StreamHandler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
