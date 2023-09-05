import os
import shutil
import logging
from lxml import etree
from typing import List, Optional


class FileManager:
    @staticmethod
    def clean_folder(folder_path):
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                        logging.debug(f'Successfully deleted {file_path}')
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        logging.debug(f'Successfully deleted directory {file_path}')
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

    @staticmethod
    def get_attribute(node, attr_id, default=None) -> Optional[str]:
        try:
            # Extract the value of the attribute specified by attr_id
            result = node.xpath(f"./attribute[@id='{attr_id}']/@value")
        except Exception as e:
            logging.error(f"Error in get_attribute: {e}")
            return default
        return result[0] if result else default

    @staticmethod
    def parse_lsx(file_path):
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            return None
        try:
            # Initialize parser and parse the XML
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(file_path, parser)
            root = tree.getroot()
            # Log successful parsing
            logging.info(f"Successfully parsed {file_path}")
            return root
        except Exception as e:
            logging.error(f"Error in parse_lsx: {e}")
            return None

    @staticmethod
    def load_nodes(lsx_file_path, node_name, attribute_list, child_handler=None):
        try:
            root = FileManager.parse_lsx(lsx_file_path)
            if root is None:
                logging.error("Failed to parse LSX file")
                return []

            nodes_data = []
            for node in root.xpath(f".//node[@id='{node_name}']"):
                node_data = {attr: FileManager.get_attribute(node, attr) for attr in attribute_list}

                if child_handler:
                    child_handler(node, node_data)

                nodes_data.append(node_data)

            return nodes_data if nodes_data else []

        except Exception as e:
            logging.error(f"An error occurred in load_from_lsx: {e}")
            return []

    @staticmethod
    def create_file(file_path):
        # Log the file path for debugging
        logging.debug(f"Trying to create file at {file_path}")

        # Create directories if they don't exist
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                logging.info(f"Created directory {directory}")
            except Exception as e:
                logging.error(f"Failed to create directory {directory}: {e}")
                return False

        # Create file if it doesn't exist
        if not os.path.exists(file_path):
            try:
                open(file_path, 'w').close()
                logging.info(f"Created file {file_path}")
                return True
            except Exception as e:
                logging.error(f"Failed to create file {file_path}: {e}")
                return False
        else:
            logging.info(f"File {file_path} already exists")
            return True

    @staticmethod
    def write_file(file_path, content):
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            logging.info(f"Wrote content to {file_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to write to file {file_path}: {e}")
            return False
