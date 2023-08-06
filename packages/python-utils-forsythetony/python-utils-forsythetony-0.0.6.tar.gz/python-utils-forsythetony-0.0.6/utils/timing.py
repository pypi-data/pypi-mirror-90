import functools
import time
import logging

logging_format = "%(asctime)s: %(message)s"
logging.basicConfig(
    format=logging_format,
    level=logging.DEBUG,
    datefmt="%H:%M:%S"
)

def timed(func):
    
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()

        value = func(*args, **kwargs)
        
        end_time = time.perf_counter()
        total_time = end_time - start_time

        logging.info(f"Completed {func.__name__} in {total_time} seconds")

        return value

    return wrapper_timer

    