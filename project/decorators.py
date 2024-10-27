from functools import wraps
from project.log_config import logger
import os


# custom error log decorator
def log_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        file_name = os.path.basename(__file__)
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error on {func.__name__} from {file_name}:\n{e}", exc_info=True)
            raise # raises the original Exception
    return wrapper

