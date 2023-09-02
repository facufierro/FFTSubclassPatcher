# model/mod_manager.py
import os
import subprocess
import logging
from utils.settings_manager import SettingsManager
from model.mod import Mod

# Initialize the logger
logging.basicConfig(level=logging.INFO)


class ModManager:

    @staticmethod
    def find_lsx_files(mod_folder_path):
        logging.info(f"Searching for LSX files in {mod_folder_path}")
        meta_lsx_path = None
        progressions_lsx_path = None

        try:
            for root, dirs, files in os.walk(mod_folder_path):
                for filename in files:
                    if filename == 'meta.lsx':
                        meta_lsx_path = os.path.join(root, filename)
                    elif filename == 'Progressions.lsx':
                        progressions_lsx_path = os.path.join(root, filename)

            logging.debug(f"Found meta.lsx at {meta_lsx_path}")
            logging.debug(f"Found Progressions.lsx at {progressions_lsx_path}")
        except Exception as e:
            logging.error(f"An error occurred while searching for LSX files: {e}")

        return meta_lsx_path, progressions_lsx_path

    @staticmethod
    def get_all_mods_from_files():
        logging.info("Getting all mods from files")
        all_mods = []

        try:
            for mod_folder in os.listdir(SettingsManager.TEMP_DIRECTORY):
                mod_folder_path = os.path.join(SettingsManager.TEMP_DIRECTORY, mod_folder)

                meta_lsx_path, progressions_lsx_path = ModManager.find_lsx_files(mod_folder_path)

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
