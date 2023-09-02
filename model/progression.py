# model/progression.py

import logging
from utils.lsx_parser import get_attribute, parse_lsx_file, get_subclasses

# Initialize logging
logging.basicConfig(level=logging.INFO)


class Progression:
    def __init__(self, lsx_file_path=None):
        if lsx_file_path:
            logging.info(f"Initializing Progression from LSX file: {lsx_file_path}")
            self.uuid, self.name, self.table_uuid, self.level, self.progression_type, self.boosts, self.passives, self.selectors, self.subclasses = self.load_from_lsx(lsx_file_path)

    def load_from_lsx(self, lsx_file_path):
        # logging.info(f"Loading Progression data from {lsx_file_path}")
        root = parse_lsx_file(lsx_file_path)

        if root is None:
            logging.error("Failed to parse LSX file")
            return

        for prog_node in root.xpath(".//node[@id='Progression']"):
            logging.debug("Found a Progression node, extracting attributes.")
            attrs = ['UUID', 'Name', 'TableUUID', 'Level', 'ProgressionType', 'Boosts', 'PassivesAdded', 'Selectors']

            uuid, name, table_uuid, level, progression_type, boosts, passives, selectors = [
                get_attribute(prog_node, attr) or {} for attr in attrs
            ]

            subclasses = get_subclasses(prog_node) or []
            # logging.debug(f"Extracted subclasses: {subclasses}")

        return uuid, name, table_uuid, level, progression_type, boosts, passives, selectors, subclasses

    def load_from_node(self, prog_node):
        # logging.info("Loading Progression data from XML node")

        attrs = ['UUID', 'Name', 'TableUUID', 'Level', 'ProgressionType', 'Boosts', 'PassivesAdded', 'Selectors']
        uuid, name, table_uuid, level, progression_type, boosts, passives, selectors = [
            get_attribute(prog_node, attr) or {} for attr in attrs
        ]

        subclasses = get_subclasses(prog_node) or []
        # logging.debug(f"Extracted subclasses: {subclasses}")

        self.uuid = uuid
        self.name = name
        self.table_uuid = table_uuid
        self.level = level
        self.progression_type = progression_type
        self.boosts = boosts
        self.passives = passives
        self.selectors = selectors
        self.subclasses = subclasses

    def combine(self, other):
        logging.info(f"Combining Progression objects with UUIDs {self.uuid['value']} and {other.uuid['value']}")
        if self.uuid["value"] == other.uuid["value"]:
            for subclass in other.subclasses:
                if subclass not in self.subclasses:
                    self.subclasses.append(subclass)
                    logging.debug(f"Added subclass {subclass}")

    def __str__(self):
        subclass_nodes = ''
        for subclass in self.subclasses:
            subclass_nodes += f'<!-- {subclass["name"]} -->\n'
            subclass_nodes += f'<node id="SubClass">\n'
            subclass_nodes += f'  <attribute id="Object" type="guid" value="{subclass["uuid"]}"/>\n'
            subclass_nodes += '</node>\n'

        return (
            f'{self.comment}\n'
            '<node id="Progression">\n'
            f'  <attribute id="{self.uuid["id"]}" type="{self.uuid["type"]}" value="{self.uuid["value"]}"/>\n'
            f'  <attribute id="{self.name["id"]}" type="{self.name["type"]}" value="{self.name["value"]}"/>\n'
            f'  <attribute id="{self.table_uuid["id"]}" type="{self.table_uuid["type"]}" value="{self.table_uuid["value"]}"/>\n'
            f'  <attribute id="{self.level["id"]}" type="{self.level["type"]}" value="{self.level["value"]}"/>\n'
            f'  <attribute id="{self.progression_type["id"]}" type="{self.progression_type["type"]}" value="{self.progression_type["value"]}"/>\n'
            '  <children>\n'
            '    <node id="SubClasses">\n'
            '      <children>\n'
            f'{subclass_nodes}'
            '      </children>\n'
            '    </node>\n'
            '  </children>\n'
            '</node>'
        )
