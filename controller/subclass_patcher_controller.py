import os
from utils.settings_manager import SettingsManager
from model.mod import Mod
from model.mod_manager import ModManager


class SubclassPatcherController:
    def __init__(self):
        # Initialize SettingsManager
        self.settings_manager = SettingsManager()

    def fetch_divine_directory(self):
        # Fetch the DIVINE_DIRECTORY path
        return self.settings_manager.DIVINE_DIRECTORY

    def save_divine_directory(self, path):
        # Save the DIVINE_DIRECTORY path
        self.settings_manager.set_divine_directory(path)

    def load_all_mods_from_mods_directory(self):
        # Load all mods from MODS_DIRECTORY
        return ModManager.get_all_mods()

    def get_mod_full_paths(self, selected_indices):
        # Get full paths of mods based on selected indices
        all_mods = self.load_all_mods_from_mods_directory()
        selected_mod_paths = [os.path.join(SettingsManager.MODS_DIRECTORY, all_mods[i]) for i in selected_indices]
        return selected_mod_paths

    def unpack_mod(self, mod_path):
        # Unpack a single mod
        return ModManager.unpack_mod(mod_path)

    def unpack_selected_mods(self, mod_paths):
        # Unpack selected mods
        for mod_path in mod_paths:
            if not ModManager.unpack_mod(mod_path):
                return False  # Return false if unpacking failed
        return True  # Return true if all unpacking succeeded

    def load_all_mods_from_temp_directory(self):
        # Load all mods from TEMP_DIRECTORY
        return ModManager.get_all_mods_from_files()

    def create_mod_patch(self, selected_mod_paths):
        # Create a patch using selected mods

        # Step 1: Unpack selected mods
        if not self.unpack_selected_mods(selected_mod_paths):
            return False  # Return false if unpacking failed

        # Step 2: Load
        self.load_all_mods_from_temp_directory()

        # Step 3: Process the mods
        # (To be implemented)

        # Step 4: Repack the mods
        # (To be implemented)

        # Step 5: Move them to OUTPUT_DIRECTORY
        # (To be implemented)

        return True  # Return true if patching succeeded
