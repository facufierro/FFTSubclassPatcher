# model/mod_manager.py
import os
from utils.settings_manager import SettingsManager


class ModManager:

    @staticmethod
    def get_all_mods():
        lstMods = []
        mods_directory = SettingsManager.MODS_DIRECTORY

        try:
            for filename in os.listdir(mods_directory):
                if filename.endswith(".pak"):
                    lstMods.append(filename)
        except Exception as e:
            print(f"An error occurred: {e}")

        return lstMods
