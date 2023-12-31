# controller/subclass_patcher_controller.py
import os
import logging
import subprocess
from typing import List, Optional
from utils.settings_manager import SettingsManager
from model.mod import Mod
from utils.mod_manager import ModManager
from utils.file_manager import FileManager


class SubclassPatcherController:
    def __init__(self, view, settings_manager: Optional[SettingsManager] = None):
        # Initialize SettingsManager and View
        self.view = view
        self.settings_manager = settings_manager if settings_manager else SettingsManager()

    def setup_mod_progress(self, mod):
        mod.add_progress_callback(self.view.update_progress_bar)

    def fetch_divine_directory(self) -> str:
        # Fetch the DIVINE_DIRECTORY path
        return self.settings_manager.DIVINE_DIRECTORY

    def save_divine_directory(self, path: str):
        # Save the DIVINE_DIRECTORY path
        self.settings_manager.set_divine_directory(path)

    def load_all_mods_from_mods_directory(self) -> List[str]:
        # Load all mods from MODS_DIRECTORY
        return ModManager.get_all_mods()

    def get_mod_full_paths(self, selected_indices: List[int]) -> List[str]:
        # Get full paths of mods based on selected indices
        all_mods = self.load_all_mods_from_mods_directory()
        selected_mod_paths = [os.path.join(SettingsManager.MODS_DIRECTORY, all_mods[i]) for i in selected_indices]
        return selected_mod_paths

    def unpack_mod(self, mod_path: str) -> bool:
        # Unpack a single mod
        return ModManager.unpack_mod(mod_path)

    def unpack_selected_mods(self, mod_paths: List[str]) -> bool:
        # Unpack selected mods
        for mod_path in mod_paths:
            if not ModManager.unpack_mod(mod_path):
                return False  # Return false if unpacking failed
        return True  # Return true if all unpacking succeeded

    def load_all_mods_from_temp_directory(self) -> List[Mod]:
        # Load all mods from TEMP_DIRECTORY
        return ModManager.get_all_mods_from_files()

    def check_and_update_create_patch_button(self):
        divine_path = self.fetch_divine_directory()
        if divine_path:
            self.view.enable_create_patch_button(True)
        else:
            self.view.enable_create_patch_button(False)

    def open_output_folder(self):
        subprocess.run(f'explorer {SettingsManager.OUTPUT_DIRECTORY}')

    def create_mod_patch(self, selected_mod_paths: List[str]) -> bool:
        # Create a mod patch using the selected mods

        # Step 0: Clean TEMP_DIRECTORY
        FileManager.clean_folder(SettingsManager.TEMP_DIRECTORY)
        # Step 1: Unpack selected mods
        if not self.unpack_selected_mods(selected_mod_paths):
            return False  # Return false if unpacking failed

        # Step 2: Load all mods from TEMP_DIRECTORY
        mods = self.load_all_mods_from_temp_directory()
        logging.info(f"Loaded {len(mods)} mods from TEMP_DIRECTORY")
        # logging.debug(f"{mods[0].progressions_string()}")

        # Step 3: Process the mods into a single patch
        patch = ModManager.combine_mods(mods)
        # logging.info(patch.progressions_string())

        # Setp 4: Create patch folders and files in TEMP_DIRECTORY (TODO: Implement this step)
        ModManager.create_patch_folder(patch)

        # Step 5: Repack the mods to OUTPUT_DIRECTORY (TODO: Implement this step)
        patch_path = os.path.join(SettingsManager.TEMP_DIRECTORY, patch.folder)
        ModManager.pack_mod(patch_path)
        return True  # Return true if patching succeeded
