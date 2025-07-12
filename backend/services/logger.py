from loguru import logger
import sys

def setup_logger():
    logger.remove()
    logger.add(sys.stdout, format="{time} | {level} | {message}", level="INFO")
    logger.info("Logger is configured.")
