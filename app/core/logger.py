from loguru import logger
from datetime import datetime
from app.core import settings
import sys

logger.remove()

log_filename = datetime.now().strftime(f"logs/{settings.logfile_naming_format}.log")
dump_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | module:{name} | method:{function} | line:{line} | {message}"


logger.add(
    sys.stdout,
    level="DEBUG",
    format=dump_format,
)


logger.add(
    log_filename,
    rotation=f"{settings.logfile_rotation_mb} MB",
    retention=f"{settings.logfile_retention_days} days",
    compression=settings.logfile_compression,
    level=settings.dump_logs_level,
    enqueue=True,
    format=dump_format,
)


def log_by_status(status_code: int, message: str = "") -> None:
    """Log a message with a level based on HTTP status code."""

    if 500 <= status_code <= 599:
        logger.critical(message)
    elif 400 <= status_code <= 499:
        logger.warning(message)
    else:
        logger.info(message)
