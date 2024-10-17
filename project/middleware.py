from fastapi import Request
from project.log_config import logger
import time

async def log_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    log_dict = {
        'url': request.url.path,
        'method': request.method,
        'process_time': round(process_time, 2)
    }
    # "extra" key word makes the dict keys recognized as
    # keys instead of normal string in log managers
    logger.info(log_dict, extra=log_dict)
    return response