# model/mod.py
import logging
from model.progression import Progression
from utils.file_manager import FileManager

# Initialize logging
logging.basicConfig(level=logging.INFO)  # Adjust level as needed


class Mod:
    def __init__(self, meta_lsx_file_path=None, progressions_lsx_file_path=None, class_descriptions_path=None):
        logging.debug("Mod constructor called")
        self.uuid = "c0d54727-cce1-4da4-b5b7-180590fb2780"
        self.name = "FFTSubclassPatch"
        self.author = "fierrof"
        self.folder = "FFTSubclassPatch"
        self.description = "A compatibility patch for subclasses in Baldur's Gate 3."
        self.progressions = []
        self.class_descriptions_path = None
        if meta_lsx_file_path and progressions_lsx_file_path:
            self.meta_lsx_file_path = meta_lsx_file_path
            self.progressions_lsx_file_path = progressions_lsx_file_path
            if class_descriptions_path is not None:
                self.class_descriptions_path = class_descriptions_path
            self.load_meta()
            self.load_progressions()
            logging.info(f"{self.name} Initialized with UUID {self.uuid}")
            # logging.debug(f"{self.meta_string()}")

    def load_meta(self):
        mod_data = FileManager.load_nodes(self.meta_lsx_file_path, 'ModuleInfo', ['UUID', 'Name', 'Author', 'Folder', 'Description'])
        logging.debug(f"Returned mod_data: {mod_data}")

        self.uuid = mod_data[0].get('UUID', self.uuid)
        self.name = mod_data[0].get('Name', self.name)
        self.author = mod_data[0].get('Author', self.author)
        self.folder = mod_data[0].get('Folder', self.folder)
        self.description = mod_data[0].get('Description', self.description)

    def load_progressions(self):
        logging.debug("load_progressions method called")

        def subclass_handler(node, node_data):
            subclasses = []
            for child_node in node.xpath(".//node[@id='SubClass']"):
                uuid = FileManager.get_attribute(child_node, 'Object')
                subclasses.append({'Name': 'Base Game Subclass', 'UUID': uuid})
            node_data['SubClasses'] = subclasses

        progressions_data = FileManager.load_nodes(
            self.progressions_lsx_file_path,
            "Progression",
            ["UUID", "Name", "TableUUID", "Level", "ProgressionType", "Boosts", "PassivesAdded", "Selectors", "AllowImprovement"],
            child_handler=subclass_handler
        )
        class_description_dict = {}  # Initialize to an empty dictionary

        if self.class_descriptions_path is not None:
            class_descriptions = FileManager.load_nodes(self.class_descriptions_path, 'ClassDescription', ['UUID', 'Name'])
            class_description_dict = {desc['UUID']: desc['Name'] for desc in class_descriptions}

        self.progressions = []  # Clear existing progressions if any

        for progression_data in progressions_data:
            subclasses = progression_data.get('SubClasses', [])
            if subclasses:
                for subclass in subclasses:
                    if subclass['UUID'] in class_description_dict:
                        subclass['Name'] = class_description_dict[subclass['UUID']]

            progression = Progression(
                uuid=progression_data.get("UUID"),
                name=progression_data.get("Name"),
                table_uuid=progression_data.get("TableUUID"),
                level=progression_data.get("Level"),
                progression_type=progression_data.get("ProgressionType"),
                boosts=progression_data.get("Boosts"),
                passives_added=progression_data.get("PassivesAdded"),
                selectors=progression_data.get("Selectors"),
                allow_improvement=progression_data.get("AllowImprovement"),
                subclasses=subclasses
            )

            # logging.debug(f"Progressions data: {progressions_data}")
            self.progressions.append(progression)

        # Log the subclasses
        for mod_progression in self.progressions:
            for subclass in mod_progression.subclasses:
                logging.debug(f"Subclass Name: {subclass['Name']}, UUID: {subclass['UUID']}")

    def meta_string(self) -> str:
        return (
            f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<save>'
            f'<version major="4" minor="0" revision="0" build="49"/>'
            f'<region id="Config">'
            f'<node id="root">'
            f'<children>'
            f'<node id="Dependencies"/>'
            f'<node id="ModuleInfo">'
            f'<attribute id="Author" type="LSWString" value="{self.author}"/>'
            f'<attribute id="CharacterCreationLevelName" type="FixedString" value=""/>'
            f'<attribute id="Description" type="LSWString" value="{self.description}"/>'
            f'<attribute id="Folder" type="LSWString" value="{self.folder}"/>'
            f'<attribute id="GMTemplate" type="FixedString" value=""/>'
            f'<attribute id="LobbyLevelName" type="FixedString" value=""/>'
            f'<attribute id="MD5" type="LSString" value=""/>'
            f'<attribute id="MainMenuBackgroundVideo" type="FixedString" value=""/>'
            f'<attribute id="MenuLevelName" type="FixedString" value=""/>'
            f'<attribute id="Name" type="FixedString" value="{self.name}"/>'
            f'<attribute id="NumPlayers" type="uint8" value="4"/>'
            f'<attribute id="PhotoBooth" type="FixedString" value=""/>'
            f'<attribute id="StartupLevelName" type="FixedString" value=""/>'
            f'<attribute id="Tags" type="LSWString" value=""/>'
            f'<attribute id="Type" type="FixedString" value="Add-on"/>'
            f'<attribute id="UUID" type="FixedString" value="{self.uuid}"/>'
            f'<attribute id="Version64" type="int64" value="72057594037927936"/>'
            f'<children>'
            f'<node id="PublishVersion">'
            f'<attribute id="Version" type="int32" value="268435456"/>'
            f'</node>'
            f'<node id="Scripts"/>'
            f'<node id="TargetModes">'
            f'<children>'
            f'<node id="Target">'
            f'<attribute id="Object" type="FixedString" value="Story"/>'
            f'</node>'
            f'</children>'
            f'</node>'
            f'</children>'
            f'</node>'
            f'</children>'
            f'</node>'
            f'</region>'
            f'</save>')

    def progressions_string(self) -> str:
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<save>\n'
            '<version major="4" minor="0" revision="9" build="330"/>\n'
            '<region id="Progressions">\n'
            '<node id="root">\n'
            '<children>\n'
            f'{"".join([str(prog) for prog in self.progressions])}'
            '</children>\n'
            '</node>\n'
            '</region>\n'
            '</save>'

        )
