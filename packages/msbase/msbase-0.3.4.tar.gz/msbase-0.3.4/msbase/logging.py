import logging
import os

# https://docs.python.org/3/library/logging.html#logrecord-attributes

logging_levels = { "DEBUG" : logging.DEBUG
                 , "INFO" : logging.INFO
                 , "WARN" : logging.WARN
                 , "ERROR" : logging.ERROR
                 , "CRITICAL" : logging.CRITICAL }

def get_logger(name: str, level = logging.INFO):
    PYLOG = os.getenv("PYLOG")
    if PYLOG is not None:
        level = logging_levels[PYLOG]

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(funcName)-11s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    print(f"Set logger({name}) level={level}")
    logger.setLevel(level)
    assert logger.level == level
    return logger

logger = get_logger("default")
