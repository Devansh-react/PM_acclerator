from loguru import logger
import sys
import os


LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | " \
             "<level>{level: <8}</level> | " \
             "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - " \
             "<level>{message}</level>"


logger.remove()

# Console logging
logger.add(sys.stdout, format=LOG_FORMAT, level="DEBUG", colorize=True)


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logger.add(
    os.path.join(LOG_DIR, "weather_bot.log"),
    format=LOG_FORMAT,
    level="INFO",
    rotation="1 day",
    retention="7 days",
    compression="zip"
)

__all__ = ["logger"]
