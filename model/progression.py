# model/progression.py

import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)


class Progression:
    def __init__(self, uuid, name, table_uuid, level, progression_type, boosts=None, passives=None, selectors=None, subclasses=None):
        self.uuid = uuid
        self.name = name
        self.table_uuid = table_uuid
        self.level = level
        self.progression_type = progression_type
        self.boosts = boosts if boosts else ""
        self.passives = passives if passives else ""
        self.selectors = selectors if selectors else ""
        self.subclasses = subclasses if subclasses else []

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
