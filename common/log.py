import logging
import os
from pathlib import Path

def get_logger(arg_log_level, args_log_file, arg_disable_file_logging, arg_disable_console_logging):
    """
    Creates the logger.

    Parameters:
        arg_log_level                   (string)
        args_log_file                   (string)
        arg_disable_file_logging        (bool)
        arg_disable_console_logging    (bool)

    Returns:
        logger (logging.logger)
    """
    LOG_LEVEL_LIST = ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]
    log_level = arg_log_level
    if log_level is None:
        log_level = logging.INFO
    elif log_level.upper() not in LOG_LEVEL_LIST:
        print(f"ERROR: Log level specified '--log_file {log_level}' not valid! Please choose from {LOG_LEVEL_LIST}")
        exit(1)


    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    log_format = logging.Formatter("%(asctime)s %(filename)s -> %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    if not arg_disable_file_logging:
        if args_log_file is not None:
            log_file = Path(args_log_file)
            log_file_parent_directory = log_file.parent.absolute()
            if not os.path.isfile(log_file):
                print(f"ERROR: Log file specified '--log_file {log_file}' not found!")
                exit(1)
        else:
            if not os.path.isdir("../logs"):
                os.mkdir("../logs")
            log_file = "../logs/execution.log"
        file_logger = logging.FileHandler(log_file)
        file_logger.setLevel(log_level)
        file_logger.setFormatter(log_format)
        logger.addHandler(file_logger)

    console_logger_stream = logging.StreamHandler()
    if arg_disable_console_logging:
        console_logger_stream.setLevel(logging.ERROR)
    else:
        console_logger_stream.setLevel(log_level)
    console_logger_stream.setFormatter(log_format)
    logger.addHandler(console_logger_stream)

    return logger


if __name__ == "__main__":
    print("This is not meant to be called directly")