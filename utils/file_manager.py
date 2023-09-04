import os
import shutil
import logging
from typing import List


class FileManager:
    @staticmethod
    def clean_folder(folder_path):
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                        logging.info(f'Successfully deleted {file_path}')
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        logging.info(f'Successfully deleted directory {file_path}')
                except Exception as e:
                    logging.error(f'Failed to delete {file_path}. Reason: {e}')
        except Exception as e:
            logging.error(f'Failed to clean folder. Reason: {e}')

    @staticmethod
    def find_files(mod_folder_path, target_filenames: List[str]):
        logging.info(f"Searching for target files in {mod_folder_path}")
        found_files = {}

        try:
            for root, dirs, files in os.walk(mod_folder_path):
                for filename in files:
                    if filename in target_filenames:
                        found_files[filename] = os.path.join(root, filename)

            for target in target_filenames:
                logging.debug(f"Found {target} at {found_files.get(target, 'Not Found')}")

        except Exception as e:
            logging.error(f"An error occurred while searching for target files: {e}")

        return found_files
