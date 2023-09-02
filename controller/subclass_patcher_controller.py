# controller/subclass_patcher_controller.py
from utils.settings_manager import SettingsManager
from model.mod import Mod
from model.mod_manager import ModManager


class SubclassPatcherController:
    def __init__(self):
        self.settings_manager = SettingsManager()

    def fetch_divine_directory(self):
        return self.settings_manager.get_divine_directory()

    def save_divine_directory(self, path):
        self.settings_manager.set_divine_directory(path)

    def load_mod(self, mod_meta_lsx_path, mod_progressions_lsx_path):
        mod = Mod()
        mod.load_from_lsx(mod_meta_lsx_path)
        mod.load_progressions_from_lsx(mod_progressions_lsx_path)

    def load_all_mods(self):
        return ModManager.get_all_mods()
