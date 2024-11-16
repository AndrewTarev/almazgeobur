import sys

from src.core.config import settings
from loguru import logger


def configure_logging() -> logger:  #
    # Удаление всех зависимостей по умолчанию
    logger.remove()

    # Для вывода логов в консоль
    logger.add(
        sys.stdout,
        level=settings.logging,
        format="<yellow>{time:YYYY-MM-DD HH:mm:ss}</yellow> | "
        "<level>{level}</level> | "
        "<yellow>{message}</yellow> |"
        "<yellow>{name}</yellow>",
    )

    return logger


my_logger: logger = configure_logging()
