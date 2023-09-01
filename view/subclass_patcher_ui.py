from PyQt5 import QtCore, QtGui, QtWidgets
import logging  # Import logging for error handling

class SubclassPatcherUI(object):

    def setupUi(self, SubclassPatcherUI):
        try:
            # Initialize the main window
            SubclassPatcherUI.setObjectName("SubclassPatcherUI")
            SubclassPatcherUI.resize(600, 400)

            # Main grid layout
            self.gridLayout_3 = QtWidgets.QGridLayout(SubclassPatcherUI)
            self.gridLayout_3.setObjectName("gridLayout_3")

            # Initialize list view for mods
            self.lstMods = QtWidgets.QListView(SubclassPatcherUI)
            self.lstMods.setObjectName("lstMods")
            self.gridLayout_3.addWidget(self.lstMods, 0, 0, 1, 1)

            # Grid layout for buttons and line edit
            self.gridLayout = QtWidgets.QGridLayout()
            self.gridLayout.setObjectName("gridLayout")

            # Initialize line edit for Divine path
            self.txtDivinePath = QtWidgets.QLineEdit(SubclassPatcherUI)
            self.txtDivinePath.setObjectName("txtDivinePath")
            self.gridLayout.addWidget(self.txtDivinePath, 0, 0, 1, 1)

            # Initialize Create Patch button
            self.btnCreatePatch = QtWidgets.QPushButton(SubclassPatcherUI)
            self.btnCreatePatch.setObjectName("btnCreatePatch")
            self.gridLayout.addWidget(self.btnCreatePatch, 0, 2, 1, 1)

            # Initialize button for selecting Divine path
            self.btnDivinePath = QtWidgets.QToolButton(SubclassPatcherUI)
            self.btnDivinePath.setObjectName("btnDivinePath")
            self.gridLayout.addWidget(self.btnDivinePath, 0, 1, 1, 1)

            # Add sub-layout to main layout
            self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)

            # Translate UI and connect slots
            self.retranslateUi(SubclassPatcherUI)
            QtCore.QMetaObject.connectSlotsByName(SubclassPatcherUI)

        except Exception as e:
            logging.error(f"Error setting up UI: {e}")  # Log the error if something goes wrong

    def retranslateUi(self, SubclassPatcherUI):
        _translate = QtCore.QCoreApplication.translate
        SubclassPatcherUI.setWindowTitle(_translate("SubclassPatcherUI", "BG3 Subclass Patcher"))
        self.btnCreatePatch.setText(_translate("SubclassPatcherUI", "Create Patch"))
        self.btnDivinePath.setText(_translate("SubclassPatcherUI", "..."))
