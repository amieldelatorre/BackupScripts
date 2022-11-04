import logging
import os
from pathlib import Path

def get_logger(arg_log_level, args_log_file, arg_enable_file_logging, arg_disable_console_logging):
    """
    Creates the logger.

    Parameters:
        arg_log_level                   (string)    Log level from arguments
        args_log_file                   (string)    Path to log file from arguments
        arg_enable_file_logging         (bool)      If we should log to a file
        arg_disable_console_logging     (bool)      If we shouldn't log to console

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

    if arg_enable_file_logging:
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


def add_logger_argparse_arguments(parser):
    """
    Adds the arguments to be parsed by argparse

    Parameters:
        parser  (argparse.parser)   Parser to add the arguments to

    Returns:
        parser  (argparse.parser)
    """
    parser.add_argument(
        '--enable_file_logging',
        help="Enables the logging to a log file",
        action="store_true"
    )

    parser.add_argument(
        '--disable_console_logging',
        help="Disable the logging to console except for ERRORS. This will overwrite the --log_level argument",
        action="store_true"
    )

    parser.add_argument(
        '--log_file',
        help="Specify the path to the log file you want to write to"
    )

    parser.add_argument(
        '--log_level',
        help="Specify the log level to use from: DEBUG|INFO|WARNING|ERROR|CRITICAL. Default logging level is INFO"
    )

    return parser



if __name__ == "__main__":
    print("This is not meant to be called directly")