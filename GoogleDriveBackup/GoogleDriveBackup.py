from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from time import sleep
import sys
import shutil
import os
import argparse
import pathlib
import logging
sys.path.append('..')
from common.log import get_logger, add_logger_argparse_arguments
from common.tar import archive_and_compress

def upload(input, logger=None):
    """
    Uploads the directory or file to Google Drive after archiving, compressing and encrypting it

    Parameters:
        input   (string)            Path to the directory or file to be uploaded
        logger  (logging.logger)    Logger to log. Default value will create a logger that with level
                                                    notset. Meaning that it will not output the logs

    Returns:
        parser  (argparse.parser)
    """

    if logger is None:
        logger = logging.getLogger()
        logger.setLevel(logging.NOTSET)

    parent_directory = pathlib.Path(__file__).parent.resolve()
    temp_directory_name = os.path.join(parent_directory, 'temp')
    logger.info(f"Attempting to create a temporary directory {temp_directory_name}")
    temp_directory_already_exists = False

    if not os.path.isdir(temp_directory_name):
        os.mkdir(temp_directory_name)
        logger.info(f"Created a temporary directory {temp_directory_name}")
    else:
        temp_directory_already_exists = True
        logger.info(f"Did not create a temporary directory {temp_directory_name}, it already exists")

    filename = archive_and_compress(input, temp_directory_name, logger)
    full_path_to_file = os.path.join(temp_directory_name, filename)

    logger.info(f"Attempting to authenticate with Google")
    google_auth = GoogleAuth()
    google_auth.LocalWebserverAuth()
    logger.info(f"Success in authenticate with Google")

    google_drive = GoogleDrive(google_auth)

    logger.info(f"Attempting to upload the archived, compressed and encrypted file to Google Drive")
    try:
        file_to_upload = google_drive.CreateFile({'title': filename})
        file_to_upload.SetContentFile(full_path_to_file)
        file_to_upload.Upload()
        file_to_upload.content.close()
        logger.info(f"Success in uploading the archived, compressed and encrypted file to Google Drive")
    except Exception as e:
        logger.Error("Could not upload to Google Drive: " + str(e))

    try:
        logger.info(f"Attempting to delete file at {full_path_to_file}")
        os.remove(f"{full_path_to_file}")
    except PermissionError as pe:
        logger.warning(f"Error in attempt to delete file at {full_path_to_file}: " + str(pe))
    except Exception as e:
        logger.error(f"Could not delete temporary file and directory created, please manually delete at {full_path_to_file}" + str(e))
        exit(1)

    logger.info(f"Success in deleting file at {full_path_to_file}")
    if not temp_directory_already_exists:
        logger.info(f"Attempting to delete directory /{temp_directory_name}")
        try:
            shutil.rmtree(temp_directory_name)
            logger.info(f"Success in deleting directory at /{temp_directory_name}")
        except Exception as e:
            logger.error(f"Could not delete temporary directory created, please manually delete at /{filename}" + str(e))


def get_google_drive_arg_parser():
    """
    Create the argument parser for uploading files to Google Drive.

    Returns:
        parser  (argparse.parser)
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-i',
        '--input',
        help="The input path to backup",
        required=True
    )

    return parser

if __name__ == "__main__":
    parser = get_google_drive_arg_parser()
    parser = add_logger_argparse_arguments(parser)
    args = parser.parse_args()

    logger = get_logger(args.log_level, args.log_file, args.enable_file_logging, args.disable_console_logging)

    upload(args.input, logger)
