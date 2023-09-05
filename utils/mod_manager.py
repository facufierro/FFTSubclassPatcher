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
                target_files = FileManager.find_files(mod_folder_path, ['meta.lsx', 'Progressions.lsx', 'ClassDescriptions.lsx'])
                meta_path = target_files.get('meta.lsx')
                progressions_path = target_files.get('Progressions.lsx')
                class_descriptions_path = target_files.get('ClassDescriptions.lsx')

                if meta_path and progressions_path:
                    logging.debug(f"Creating mod object for {mod_folder}")
                    mod = Mod(meta_path, progressions_path, class_descriptions_path)
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
    def create_patch_folder(patch):
        meta_file_path = os.path.join(SettingsManager.TEMP_DIRECTORY, patch.folder, "Mods", patch.folder, "meta.lsx")
        if FileManager.create_file(meta_file_path):
            if FileManager.write_file(meta_file_path, patch.meta_string()):
                logging.info("Successfully created and wrote to meta file.")
            else:
                logging.error("Failed to write to meta file.")
        else:
            logging.error("Failed to create meta file.")
        # create Progressions.lsx
        progressions_file_path = os.path.join(SettingsManager.TEMP_DIRECTORY, patch.folder, "Public", patch.folder, "Progressions", "Progressions.lsx")
        if FileManager.create_file(progressions_file_path):
            if FileManager.write_file(progressions_file_path, patch.progressions_string()):
                logging.info("Successfully created and wrote to progressions file.")
            else:
                logging.error("Failed to write to progressions file.")
        else:
            logging.error("Failed to create progressions file.")

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
            if mod.progressions is not None:
                for progression in mod.progressions:

                    # Check if this progression already exists in patch
                    existing_progression = next((p for p in patch.progressions if p.uuid == progression.uuid), None)

                    if existing_progression:
                        # Merge subclasses if progression already exists
                        existing_subclass_uuids = {s['UUID'] for s in existing_progression.subclasses}
                        new_subclasses = [s for s in progression.subclasses if s['UUID'] not in existing_subclass_uuids]
                        existing_progression.subclasses.extend(new_subclasses)

                        # Merge all attributes
                        for attr in ['boosts', 'passives_added', 'passives_removed' 'selectors', 'allow_improvement', 'is_multiclass']:  # Add more attributes here as needed
                            existing_attr_value = getattr(existing_progression, attr, None)
                            new_attr_value = getattr(progression, attr, None)

                            if existing_attr_value in [None, ""] or new_attr_value in [None, ""]:
                                continue  # Skip merging for this attribute
                            existing_attr_values = set(existing_attr_value.split(';'))
                            new_attr_values = set(new_attr_value.split(';'))
                            merged_attr_values = existing_attr_values.union(new_attr_values)
                            setattr(existing_progression, attr, ';'.join(merged_attr_values))

                    else:
                        # Add the whole progression if it doesn't exist
                        patch.progressions.append(progression)
            else:
                logging.warning(f"No progressions in mod: {mod.name}")
        return patch

    @staticmethod
    def pack_mod(mod_folder_path):
        try:
            # Reload settings to ensure DIVINE_DIRECTORY is up-to-date
            SettingsManager._instance.load_settings()

            if SettingsManager.DIVINE_DIRECTORY is None:
                # logging.error("DIVINE_DIRECTORY is not set.")
                return False

            # Create a .pak file name based on the mod folder name
            pak_file_name = "FFTSubclassPatch.pak"

            # Join this file name with your OUTPUT_DIR to get the full path
            pak_file_path = os.path.join(SettingsManager.OUTPUT_DIRECTORY, pak_file_name)

            command = [
                SettingsManager.DIVINE_DIRECTORY,
                "-g",
                "bg3",  # Replace this with the appropriate game if needed
                "--action",
                "create-package",
                "--source",
                mod_folder_path,
                "--destination",
                pak_file_path,
                "-l",
                "all",
            ]
            subprocess.run(command, check=True)
            return True
        except Exception as e:
            logging.error(
                f"Failed to pack {mod_folder_path} to {pak_file_path}: {e}")
            return False
