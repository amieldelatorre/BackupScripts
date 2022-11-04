import logging

from log import get_logger, add_logger_argparse_arguments
from datetime import datetime
import argparse
import os
import tarfile


def archive_and_compress(source, output_directory, logger=logging.getLogger(__name__).setLevel(logging.NOTSET)):
    """
    Archive and compress a directory or file.

    Parameters:
        source              (string)            Path to the directory or file to archive and compress
        output_directory    (string)            Path to the directory of where to store the .tar.gz file to be created
        logger              (logging.logger)    Logger to log. Default value will create a logger that with level
                                                    notset. Meaning that it will not output the logs

    Returns:
        None
    """
    datetime_now = datetime.now()
    datetime_string = datetime_now.strftime("%Y%m%d-%H%M%S")
    complete_output_path = f"{output_directory}/{datetime_string}-{os.path.basename(source)}.tar.gz"
    logger.info(f"Attempting to archive and compress {source} to {complete_output_path}")

    try:
        with tarfile.open(complete_output_path, "w:gz") as tar:
            tar.add(source, arcname=os.path.basename(source))
    except Exception as e:
        logger.error(f"Failed in attempt to archive and compress: {str(e)}")
    else:
        logger.info(f"Success in archiving and compressing {source} to {complete_output_path}")


def extract(filename, output_directory, logger=logging.getLogger(__name__).setLevel(logging. NOTSET)):
    """
    Extract an archived and compressed file.

    Parameters:
        filename            (string)            Path to the directory or file to extract
        output_directory    (string)            Path of the directory to extract to
        logger              (logging.logger)    Logger to log. Default value will create a logger that with level
                                                    notset. Meaning that it will not output the logs

    Returns:
        None
    """
    logger.info(f"Attempting to extract {filename} to {output_directory}")
    try:
        with tarfile.open(filename) as tar:
            tar.extractall(path=output_directory)
    except Exception as e:
        logger.error(f"Failed in attempt to extract: {str(e)}")
    else:
        logger.info(f"Success in extracting {filename} to {output_directory}")


def get_tar_arg_parser():
    parser = argparse.ArgumentParser()

    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        '--archive_and_compress',
        action='store_true',
        help="Archive and compress the specified path"
    )
    action_group.add_argument(
        '--extract',
        action='store_true',
        help="Extract the specified .tar.gz file"
    )

    parser.add_argument(
        '-i',
        '--input',
        help="The input path to archive and compress or extract",
        required=True
    )
    parser.add_argument(
        '-o',
        '--output',
        help="The output path to store archived and compressed files or extracted files",
        required=True
    )

    return parser


if __name__ == "__main__":
    parser = get_tar_arg_parser()
    parser = add_logger_argparse_arguments(parser)
    args = parser.parse_args()

    logger = get_logger(args.log_level, args.log_file, args.enable_file_logging, args.disable_console_logging)

    if args.archive_and_compress and not args.extract:
        archive_and_compress(args.input, args.output, logger)
    elif not args.archive_and_compress and args.extract:
        extract(args.input, args.output, logger)
    else:
        logger.error("Honestly, I don't know how you got here")



