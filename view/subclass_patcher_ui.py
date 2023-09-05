
# view/subclass_patcher_ui.py
from PyQt5.QtCore import QMetaObject, QCoreApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QFileDialog, QGridLayout, QListView, QLineEdit, QPushButton, QToolButton, QAbstractItemView, QMessageBox, QProgressBar
import logging  # Import logging for error handling
from controller.subclass_patcher_controller import SubclassPatcherController  # Import the controller
from utils.file_manager import FileManager  # Import the file manager
from utils.settings_manager import SettingsManager  # Import the settings manager


class SubclassPatcherUI(object):
    def __init__(self):
        self.controller = SubclassPatcherController(self)
        # Connect the aboutToQuit signal to clean_folder
        QCoreApplication.instance().aboutToQuit.connect(lambda: FileManager.clean_folder(SettingsManager.TEMP_DIRECTORY))

    def setupUi(self, SubclassPatcherUI):
        try:
            # Initialize the main window
            SubclassPatcherUI.setObjectName("SubclassPatcherUI")
            SubclassPatcherUI.resize(600, 400)

            # Main grid layout
            self.gridLayout_3 = QGridLayout(SubclassPatcherUI)
            self.gridLayout_3.setObjectName("gridLayout_3")

            # Initialize list view for mods
            self.lstMods = QListView(SubclassPatcherUI)
            self.lstMods.setObjectName("lstMods")

            # Set selection mode
            self.lstMods.setSelectionMode(QAbstractItemView.MultiSelection)  # Or QAbstractItemView.ExtendedSelection
            self.gridLayout_3.addWidget(self.lstMods, 0, 0, 1, 1)
            # Initialize the model for lstMods
            self.model = QStandardItemModel(self.lstMods)

            # Update the mod list
            self.update_mod_list()

            # Grid layout for buttons and line edit
            self.gridLayout = QGridLayout()
            self.gridLayout.setObjectName("gridLayout")

            # Initialize line edit for Divine path
            self.txtDivinePath = QLineEdit(SubclassPatcherUI)
            self.txtDivinePath.setObjectName("txtDivinePath")
            self.txtDivinePath.setPlaceholderText("Choose divine.exe path")  # Set placeholder text
            self.gridLayout.addWidget(self.txtDivinePath, 0, 0, 1, 1)

            # Fetch divine directory from the controller and set it to txtDivinePath
            divine_path = self.controller.fetch_divine_directory()
            self.txtDivinePath.setText(divine_path)

            # Initialize Create Patch button
            self.btnCreatePatch = QPushButton(SubclassPatcherUI)
            self.btnCreatePatch.setObjectName("btnCreatePatch")
            self.gridLayout.addWidget(self.btnCreatePatch, 0, 2, 1, 1)

            # Connect Create Patch button to initiate the mod patching process
            self.btnCreatePatch.clicked.connect(self.initiate_mod_patching)

            # Initialize button for selecting Divine path
            self.btnDivinePath = QToolButton(SubclassPatcherUI)
            self.btnDivinePath.setObjectName("btnDivinePath")
            self.gridLayout.addWidget(self.btnDivinePath, 0, 1, 1, 1)

            # Connect btnDivinePath to open the directory browser
            self.btnDivinePath.clicked.connect(self.browse_divine_directory)

            # Add sub-layout to main layout
            self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)

            # Translate UI and connect slots
            self.retranslateUi(SubclassPatcherUI)
            QMetaObject.connectSlotsByName(SubclassPatcherUI)

            # Now that all UI elements are initialized, check for DIVINE_DIRECTORY
            divine_path = self.controller.fetch_divine_directory()
            if not divine_path:
                self.show_divine_directory_prompt()

            # Update the Create Patch button state
            self.controller.check_and_update_create_patch_button()
        except Exception as e:
            logging.error(f"Error setting up UI: {e}")  # Log the error if something goes wrong

    def show_divine_directory_prompt(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Choose your divine.exe file directory.")
        msg.setWindowTitle("Divine Directory Required")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()  # This will block until the user clicks 'OK'
        self.browse_divine_directory()

    def enable_create_patch_button(self, enable: bool):
        self.btnCreatePatch.setEnabled(enable)

    def retranslateUi(self, SubclassPatcherUI):
        _translate = QCoreApplication.translate
        SubclassPatcherUI.setWindowTitle(_translate("SubclassPatcherUI", "BG3 Subclass Patcher"))
        self.btnCreatePatch.setText(_translate("SubclassPatcherUI", "Create Patch"))
        self.btnDivinePath.setText(_translate("SubclassPatcherUI", "..."))

    def browse_divine_directory(self):
        # Open a file dialog to select divine.exe
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Select divine.exe File",
            "",
            "Executable Files (*.exe);;All Files (*)",
            options=options
        )

        if file_path.lower().endswith('divine.exe'):
            self.txtDivinePath.setText(file_path)
            self.controller.save_divine_directory(file_path)
            self.controller.check_and_update_create_patch_button()
        else:
            # Show a dialog to inform the user that they didn't select 'divine.exe'
            QMessageBox.critical(None, 'Invalid File', 'Invalid file selected. Please select divine.exe.')

    def update_mod_list(self):
        self.model.clear()
        mod_list = self.controller.load_all_mods_from_mods_directory()

        for mod in mod_list:
            # print(type(mod))  # Print the type of mod to the console for debugging
            item = QStandardItem(mod)
            self.model.appendRow(item)

        self.lstMods.setModel(self.model)

    def initiate_mod_patching(self):
        # Get the selected mod indices first
        selected_mod_indices = self.get_selected_mod_indices()

        # Use the controller to get the full paths of selected mods
        selected_mod_paths = self.controller.get_mod_full_paths(selected_mod_indices)

        if self.controller.create_mod_patch(selected_mod_paths):  # Assuming create_mod_patch returns a boolean indicating success
            self.controller.open_output_folder()

    def get_selected_mod_indices(self):
        # Fetch the selected mod indices from lstMods
        selected_indexes = self.lstMods.selectionModel().selectedIndexes()
        selected_mod_indices = [index.row() for index in selected_indexes]
        return selected_mod_indices
