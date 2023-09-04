# model/mod.py
import logging
from model.progression import Progression
from utils.lsx_manager import load_from_lsx

# Initialize logging
logging.basicConfig(level=logging.INFO)  # Adjust level as needed


class Mod:
    def __init__(self, meta_lsx_file_path=None, progressions_lsx_file_path=None):
        self.uuid = "c0d54727-cce1-4da4-b5b7-180590fb2780"
        self.name = "FFTSubclassPatch"
        self.author = "fierrof"
        self.folder = "FFTSubclassPatch"
        self.progressions = []

        if meta_lsx_file_path is not None and progressions_lsx_file_path is not None:
            self.meta_lsx_file_path = meta_lsx_file_path
            self.progressions_lsx_file_path = progressions_lsx_file_path
            self.load_meta()
            self.load_progressions()
            logging.info(f"{self.name} Initialized with UUID {self.uuid}")

    def load_meta(self):
        mod_data = load_from_lsx(self.meta_lsx_file_path, 'ModuleInfo', ['UUID', 'Name', 'Author', 'Folder'])
        self.uuid = mod_data[0][0]
        self.name = mod_data[0][1]
        self.author = mod_data[0][2]
        self.folder = mod_data[0][3]

    def load_progressions(self):
        if self.progressions_lsx_file_path:
            try:
                progressions_data = load_from_lsx(self.progressions_lsx_file_path, "Progression", ["UUID", "Name", "TableUUID", "Level", "ProgressionType", "Boosts", "PassivesAdded", "Selectors"], "SubClass")
                for progression_data in progressions_data:
                    progression = Progression(progression_data[0], progression_data[1], progression_data[2], progression_data[3], progression_data[4], progression_data[5], progression_data[6], progression_data[7], progression_data[8])
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
            f'<attribute id="Author" type="LSWString" value="{self.name}"/>'
            f'<attribute id="CharacterCreationLevelName" type="FixedString" value=""/>'
            f'<attribute id="Description" type="LSWString" value="{self.folder}"/>'
            f'<attribute id="Folder" type="LSWString" value="{self.folder}"/>'
            f'<attribute id="GMTemplate" type="FixedString" value=""/>'
            f'<attribute id="LobbyLevelName" type="FixedString" value=""/>'
            f'<attribute id="MD5" type="LSString" value=""/>'
            f'<attribute id="MainMenuBackgroundVideo" type="FixedString" value=""/>'
            f'<attribute id="MenuLevelName" type="FixedString" value=""/>'
            f'<attribute id="Name" type="FixedString" value="{self.folder}"/>'
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
