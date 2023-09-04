# model/mod_manager.py
import os
import subprocess
import logging
from model.mod import Mod
from utils.settings_manager import SettingsManager
from utils.file_manager import FileManager


# Initialize the logger
logging.basicConfig(level=logging.INFO)


class ModManager:

    @staticmethod
    def get_all_mods_from_files():
        logging.info("Getting all mods from files")
        all_mods = []

        try:
            for mod_folder in os.listdir(SettingsManager.TEMP_DIRECTORY):
                mod_folder_path = os.path.join(SettingsManager.TEMP_DIRECTORY, mod_folder)
                target_files = FileManager.find_files(mod_folder_path, ['meta.lsx', 'Progressions.lsx'])
                meta_lsx_path = target_files.get('meta.lsx')
                progressions_lsx_path = target_files.get('Progressions.lsx')

                if meta_lsx_path and progressions_lsx_path:
                    logging.debug(f"Creating mod object for {mod_folder}")
                    mod = Mod(meta_lsx_path, progressions_lsx_path)
                    all_mods.append(mod)
                else:
                    logging.warning(f"Could not find required LSX files for mod {mod_folder}")
        except Exception as e:
            logging.error(f"An error occurred while getting all mods from files: {e}")

        return all_mods

    @staticmethod
    def get_all_mods():
        lstMods = []
        mods_directory = SettingsManager.MODS_DIRECTORY

        try:
            for filename in os.listdir(mods_directory):
                if filename.endswith(".pak"):
                    lstMods.append(filename)
                    logging.debug(f"Identified mod file: {filename}")
        except Exception as e:
            logging.error(f"An error occurred while listing all mods: {e}")

        return lstMods

    @staticmethod
    def unpack_mod(mod_path):
        try:
            divine_dir = SettingsManager().DIVINE_DIRECTORY
            temp_dir = SettingsManager.TEMP_DIRECTORY
            logging.info(f"Preparing to unpack {mod_path} using Divine tool from {divine_dir} to {temp_dir}")

            command = [
                divine_dir,
                "-g",
                "bg3",
                "--action",
                "extract-package",
                "--source",
                mod_path,
                "--destination",
                temp_dir,
                "-l",
                "all",
                "--use-package-name",
            ]
            subprocess.run(command, check=True)
            logging.info(f"Successfully unpacked {mod_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to unpack {mod_path}: {e}")
            return False

    @staticmethod
    def combine_mods(mods):
        patch = Mod()
        for mod in mods:
            if mod.progressions is not None:  # Check if progressions is None
                for progression in mod.progressions:
                    if progression.subclasses:
                        patch.progressions.append(progression)
                        logging.debug(f"Added progression {progression.name}")
                        logging.debug(f"{progression.__str__()}")
            else:
                logging.warning(f"No progressions in mod: {mod.name}")
        return patch
