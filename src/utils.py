import sys
import logging


def get_logger(name, level=logging.ERROR, stream_level=logging.ERROR):
    log_file = "results.log"
    file_handler = logging.FileHandler(log_file)
    stream_handler = logging.StreamHandler(sys.stdout)
    file_handler.setLevel(level)
    stream_handler.setLevel(stream_level)
    # formatting for loggers
    file_handler_format = logging.Formatter("%(levelname)s - %(asctime)s - %(message)s")
    stream_handler_format = logging.Formatter("%(levelname)s - %(asctime)s - %(message)s")
    file_handler.setFormatter(file_handler_format)
    stream_handler.setFormatter(stream_handler_format)

    logger = logging.getLogger(name)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(level)
    return logger
