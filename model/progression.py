# model/progression.py

import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)


class Progression:
    def __init__(self, uuid, name, table_uuid, level, progression_type, boosts=None, passives=None, selectors=None, allow_improvement=None, subclasses=None):
        self.uuid = uuid
        self.name = name
        self.table_uuid = table_uuid
        self.level = level
        self.progression_type = progression_type
        self.boosts = boosts if boosts else ""
        self.passives = passives if passives else ""
        self.selectors = selectors if selectors else ""
        self.allow_improvement = allow_improvement if allow_improvement else ""
        self.subclasses = subclasses if subclasses else []

    def __str__(self):
        subclass_nodes = ''
        if self.subclasses:
            for subclass in self.subclasses:
                subclass_nodes += f'<!-- {subclass["Name"]} -->\n'
                subclass_nodes += f'<node id="SubClass">\n'
                subclass_nodes += f'  <attribute id="Object" type="guid" value="{subclass["UUID"]}"/>\n'
                subclass_nodes += '</node>\n'
            subclass_nodes = (
                '  <children>\n'
                '    <node id="SubClasses">\n'
                '      <children>\n'
                f'{subclass_nodes}'
                '      </children>\n'
                '    </node>\n'
                '  </children>\n'
            )
        else:
            subclass_nodes = ''
        optional_attributes = []
        if self.boosts != "":
            optional_attributes.append(f'  <attribute id="Boosts" type="LSString" value="{self.boosts}"/>\n')
        if self.passives != "":
            optional_attributes.append(f'  <attribute id="Passives" type="LSString" value="{self.passives}"/>\n')
        if self.selectors != "":
            optional_attributes.append(f'  <attribute id="Selectors" type="LSString" value="{self.selectors}"/>\n')
        if self.allow_improvement != "":
            optional_attributes.append(f'  <attribute id="AllowImprovement" type="bool" value="{self.allow_improvement}"/>\n')
        return (
            f'<!-- {self.name} -->\n'
            '<node id="Progression">\n'
            f'  <attribute id="UUID" type="guid" value="{self.uuid}"/>\n'

            f'  <attribute id="Name" type="LSString" value="{self.name}"/>\n'
            f'  <attribute id="TableUUID" type="guid" value="{self.table_uuid}"/>\n'
            f'  <attribute id="Level" type="uint8" value="{self.level}"/>\n'
            f'  <attribute id="ProgressionType" type="uint8" value="{self.progression_type}"/>\n'
            f'{"".join(optional_attributes)}'
            f'{subclass_nodes}'
            '</node>'
        )
