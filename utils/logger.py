import logging
from typing import Optional

def setup_logger(name: str = None, level: int = logging.INFO, log_file: Optional[str] = None,) -> logging.Logger:
    """
    Sets up and returns a logger.

    Args:
        name (Optional[str]): Name of the logger. If None, the root logger is used. Defaults to None.
        level (int, optional): The minimum log level for the logger (e.g., logging.INFO, logging.DEBUG). Defaults to logging.INFO.
        log_file (Optional[str], optional): If provided, logs will be written to this file. Otherwise, logs are output to the console. Defaults to None.

    Returns:
        logging.Logger: The configured logger instance.
    """
    # get a logger with a specified name. Else get the root logger
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
