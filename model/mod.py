# model/mod.py
import logging
from model.progression import Progression
from utils.file_manager import FileManager

# Initialize logging
logging.basicConfig(level=logging.INFO)  # Adjust level as needed


class Mod:
    def __init__(self, meta_lsx_file_path=None, progressions_lsx_file_path=None):
        self.uuid = "c0d54727-cce1-4da4-b5b7-180590fb2780"
        self.name = "FFTSubclassPatch"
        self.author = "fierrof"
        self.folder = "FFTSubclassPatch"
        self.progressions = []

        if meta_lsx_file_path and progressions_lsx_file_path:
            self.meta_lsx_file_path = meta_lsx_file_path
            self.progressions_lsx_file_path = progressions_lsx_file_path
            self.load_meta()
            self.load_progressions()
            logging.info(f"{self.name} Initialized with UUID {self.uuid}")
            logging.debug(f"{self.meta_string()}")

    def load_meta(self):
        mod_data = FileManager.load_nodes(self.meta_lsx_file_path, 'ModuleInfo', ['UUID', 'Name', 'Author', 'Folder'])
        logging.debug(f"Returned mod_data: {mod_data}")

        self.uuid = mod_data[0].get('UUID', self.uuid)
        self.name = mod_data[0].get('Name', self.name)
        self.author = mod_data[0].get('Author', self.author)
        self.folder = mod_data[0].get('Folder', self.folder)

    def load_progressions(self):
        if self.progressions_lsx_file_path:
            try:
                progressions_data = FileManager.load_nodes(
                    self.progressions_lsx_file_path,
                    "Progression",
                    ["UUID", "Name", "TableUUID", "Level", "ProgressionType", "Boosts", "PassivesAdded", "Selectors"],
                    child_node_name="SubClass",
                    child_key_attr="Name",
                    child_value_attr="UUID"
                )
                for progression_data in progressions_data:
                    progression = Progression(
                        uuid=progression_data.get("UUID"),
                        name=progression_data.get("Name"),
                        table_uuid=progression_data.get("TableUUID"),
                        level=progression_data.get("Level"),
                        progression_type=progression_data.get("ProgressionType"),
                        boosts=progression_data.get("Boosts"),
                        passives=progression_data.get("PassivesAdded"),
                        selectors=progression_data.get("Selectors"),
                        subclasses=progression_data.get("SubClass", {})
                    )
                    self.progressions.append(progression)
            except Exception as e:
                logging.error(f"An error occurred while loading progressions: {e}")
                return []

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
            f'<attribute id="Description" type="LSWString" value="{self.folder}"/>'
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

    def progressions_string(self, patch) -> str:
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<save>\n'
            '<version major="4" minor="0" revision="9" build="330"/>\n'
            '<region id="Progressions">\n'
            '<node id="root">\n'
            '<children>\n'
            f'{"".join([str(prog) for prog in patch.progressions])}'
            '</children>\n'
            '</node>\n'
            '</region>\n'
            '</save>'

        )
