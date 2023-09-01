from lxml import etree
from typing import List, Optional
import logging


def get_attribute(node, attr_id, default=None) -> Optional[str]:
    try:
        # Extract the value of the attribute specified by attr_id
        result = node.xpath(f"./attribute[@id='{attr_id}']/@value")
    except Exception as e:
        logging.error(f"Error in get_attribute: {e}")
        return default

    # Return result if found, otherwise return the default value
    return result[0] if result else default


def parse_lsx_file(file_path: str) -> Optional[etree._Element]:
    try:
        # Initialize parser and parse the XML
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(file_path, parser)
        return tree.getroot()
    except Exception as e:
        logging.error(f"Error in parse_lsx_file: {e}")
        return None


def get_subclasses(node) -> List[dict]:
    try:
        # Extract the uuid and name for each SubClass and return as a list of dictionaries
        return [
            {
                "uuid": child_node.get('value'),
                "name": None  # Replace `None` with your `read_class_descriptions` function or similar
            }
            for child_node in node.xpath(".//node[@id='SubClasses']/children/node[@id='SubClass']/attribute[@id='Object']")
        ]
    except Exception as e:
        logging.error(f"Error in get_subclasses: {e}")
        return []
