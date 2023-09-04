import os
from lxml import etree
from typing import List, Optional
import logging

from model.progression import Progression
# Configure logging
logging.basicConfig(level=logging.DEBUG)


def get_attribute(node, attr_id, default=None) -> Optional[str]:
    try:
        # Extract the value of the attribute specified by attr_id
        result = node.xpath(f"./attribute[@id='{attr_id}']/@value")
    except Exception as e:
        logging.error(f"Error in get_attribute: {e}")
        return default

    # Log the result for debugging
    # logging.debug(f"Extracted attribute {attr_id}: {result}")

    # Return result if found, otherwise return the default value
    # Note: result is a list, so we return the first element
    return result[0] if result else default


def parse_lsx_file(file_path):
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
        logging.error(f"Error in parse_lsx_file: {e}")
        return None


def load_from_lsx(lsx_file_path, node_name, attribute_list, child_node_name=None):
    try:
        root = parse_lsx_file(lsx_file_path)
        if root is None:
            logging.error("Failed to parse LSX file")
            return []

        nodes_data = []
        for node in root.xpath(f".//node[@id='{node_name}']"):
            node_data = [get_attribute(node, attr) for attr in attribute_list]
            if child_node_name:
                child_data = []
                for child_node in node.xpath(f".//node[@id='{child_node_name}']"):
                    child_attr = get_attribute(child_node, 'Object')  # Assuming the child attribute is named 'Object'
                    if child_attr:
                        child_data.append(child_attr)
                node_data.append(child_data)
            nodes_data.append(node_data)

        return nodes_data if nodes_data else []

    except Exception as e:
        logging.error(f"An error occurred in load_from_lsx: {e}")
        return []
