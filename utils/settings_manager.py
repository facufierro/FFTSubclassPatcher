import os
import json
import logging


class SettingsManager:
    _instance = None  # Singleton instance
    _settings_path = "settings.json"  # Path to settings file

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsManager, cls).__new__(cls)

            # Initialize directories
            cls.BASE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cls.TEMP_DIRECTORY = os.path.join(cls.BASE_DIRECTORY, "temp")
            cls.OUTPUT_DIRECTORY = os.path.join(cls.BASE_DIRECTORY, "output")
            cls.MODS_DIRECTORY = os.path.join(os.getenv('LOCALAPPDATA'), 'Larian Studios', 'Baldur\'s Gate 3', 'Mods')

            # Initialize settings as an empty dictionary
            cls._instance.settings = {}

            try:
                # Load settings from JSON
                cls._instance.load_settings()
            except Exception as e:
                logging.error(f"Error loading settings: {e}")

            # Get DIVINE_DIRECTORY from loaded settings
            cls.DIVINE_DIRECTORY = cls._instance.settings.get('DIVINE_DIRECTORY', None)

            # Ensure directories exist
            cls._ensure_directory_exists(cls.TEMP_DIRECTORY)
            cls._ensure_directory_exists(cls.OUTPUT_DIRECTORY)
            cls._ensure_directory_exists(cls.DIVINE_DIRECTORY)
            cls._ensure_directory_exists(cls.MODS_DIRECTORY)
        return cls._instance

    @staticmethod
    def _ensure_directory_exists(directory_path):
        # Create directory if it does not exist
        if directory_path and not os.path.exists(directory_path):
            try:
                os.makedirs(directory_path)
            except Exception as e:
                logging.error(f"Error creating directory {directory_path}: {e}")

    def load_settings(self):
        # Load settings from JSON file
        if not os.path.exists(self._settings_path):
            self.save_settings()
        else:
            try:
                with open(self._settings_path, 'r') as f:
                    self.settings = json.load(f)
            except Exception as e:
                logging.error(f"Error reading settings file: {e}")

    def save_settings(self):
        # Save settings to JSON file
        try:
            with open(self._settings_path, 'w') as f:
                json.dump(self.settings, f)
        except Exception as e:
            logging.error(f"Error writing settings file: {e}")

    def set_divine_directory(self, path):
        self.DIVINE_DIRECTORY = path
        self.set_setting('DIVINE_DIRECTORY', path)

    def set_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()
