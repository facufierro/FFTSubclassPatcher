# model/mod.py
import logging
from model.progression import Progression
from utils.lsx_parser import get_attribute, parse_lsx_file

# Initialize logging
logging.basicConfig(level=logging.INFO)


class Mod:
    def __init__(self, meta_lsx_file_path=None, progressions_lsx_file_path=None):
        if meta_lsx_file_path and progressions_lsx_file_path:
            logging.info(f"Initializing Mod with metadata from {meta_lsx_file_path} and progressions from {progressions_lsx_file_path}")
            self.uuid, self.name, self.author, self.folder = self.load_meta_from_lsx(meta_lsx_file_path)
            self.progressions = self.load_progressions_from_lsx(progressions_lsx_file_path)
        else:
            # Initialize with default values
            logging.info("Initializing Mod with default values.")
            self.uuid = "c0d54727-cce1-4da4-b5b7-180590fb2780"
            self.name = "FFTSubclassPatch"
            self.author = "fierrof"
            self.folder = "FFTSubclassPatch"
            self.progressions = []

    def load_meta_from_lsx(self, lsx_file_path):
        logging.info(f"Loading metadata from {lsx_file_path}")
        root = parse_lsx_file(lsx_file_path)
        for mod_node in root.xpath(".//node[@id='ModuleInfo']"):
            attrs = ['UUID', 'Name', 'Author', 'Folder']
            uuid, name, author, folder = [get_attribute(mod_node, attr) for attr in attrs]
        return uuid, name, author, folder

    def load_progressions_from_lsx(self, lsx_file_path):
        logging.info(f"Loading progressions from {lsx_file_path}")
        root = parse_lsx_file(lsx_file_path)
        if root is None:
            logging.error(f"Failed to parse file: {lsx_file_path}")
            return

        self.progressions = []  # Resetting the list

        for prog_node in root.xpath(".//node[@id='Progression']"):
            progression = Progression()
            progression.load_from_node(prog_node)  # Using the new method
            self.progressions.append(progression)

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
