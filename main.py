# main.py
from PyQt5 import QtWidgets
from view.subclass_patcher_ui import SubclassPatcherUI  # Replace with your actual file and class name
from utils.settings_manager import SettingsManager
from utils.debug import setup_logger
import sys

if __name__ == "__main__":
    # Initialize settings and logger
    settings_manager = SettingsManager()
    setup_logger()

    # Initialize and show the PyQt window
    app = QtWidgets.QApplication(sys.argv)
    MainUI = QtWidgets.QDialog()
    ui = SubclassPatcherUI()
    ui.setupUi(MainUI)
    MainUI.show()

    # Start the PyQt event loop
    sys.exit(app.exec_())
