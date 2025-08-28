import logging
from typing import Optional

def setup_logger(name: str = None, level: int = logging.INFO, log_file: Optional[str] = None,) -> logging.Logger:
    # get a logger with a speicifed name. Else get the root logger
    logger = logging.getLogger(name)
    # check if the logger with that name has already been assigned handlers. Else create and add the handler + set the level
    if not logger.hasHandlers():
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        else:
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        logger.setLevel(level)
    # return the configured logger
    return logger
