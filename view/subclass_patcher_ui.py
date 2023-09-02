
# view/subclass_patcher_ui.py
from PyQt5.QtCore import QMetaObject, QCoreApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QFileDialog, QGridLayout, QListView, QLineEdit, QPushButton, QToolButton, QAbstractItemView
import logging  # Import logging for error handling
from controller.subclass_patcher_controller import SubclassPatcherController  # Import the controller


class SubclassPatcherUI(object):
    def __init__(self):
        self.controller = SubclassPatcherController()

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
            self.gridLayout.addWidget(self.txtDivinePath, 0, 0, 1, 1)

            # Fetch divine directory from the controller and set it to txtDivinePath
            divine_path = self.controller.fetch_divine_directory()
            self.txtDivinePath.setText(divine_path)

            # Initialize Create Patch button
            self.btnCreatePatch = QPushButton(SubclassPatcherUI)
            self.btnCreatePatch.setObjectName("btnCreatePatch")
            self.gridLayout.addWidget(self.btnCreatePatch, 0, 2, 1, 1)

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

        except Exception as e:
            logging.error(f"Error setting up UI: {e}")  # Log the error if something goes wrong

    def retranslateUi(self, SubclassPatcherUI):
        _translate = QCoreApplication.translate
        SubclassPatcherUI.setWindowTitle(_translate("SubclassPatcherUI", "BG3 Subclass Patcher"))
        self.btnCreatePatch.setText(_translate("SubclassPatcherUI", "Create Patch"))
        self.btnDivinePath.setText(_translate("SubclassPatcherUI", "..."))

    def browse_divine_directory(self):
        # Open a directory browser dialog
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(None, "Select Divine Directory", "", options=options)

        if directory:  # If a directory is selected
            self.txtDivinePath.setText(directory)  # Set the directory path in txtDivinePath

            # Use the Controller to save the directory to settings
            self.controller.save_divine_directory(directory)

    def update_mod_list(self):
        self.model.clear()
        mod_list = self.controller.load_all_mods()

        for mod in mod_list:
            item = QStandardItem(mod)
            self.model.appendRow(item)

        self.lstMods.setModel(self.model)
