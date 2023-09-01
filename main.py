# main.py
from utils.settings_manager import SettingsManager
from utils.debug import setup_logger

if __name__ == "__main__":
    settings_manager = SettingsManager()
    setup_logger()
