import logging
import sys

logger = logging.getLogger()

formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S"
)

# handlers
console_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("logs.log")

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.handlers = [console_handler, file_handler]

logger.setLevel(logging.DEBUG)
