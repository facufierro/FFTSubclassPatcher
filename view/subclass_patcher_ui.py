from PyQt5 import QtCore, QtGui, QtWidgets
import logging  # Assuming debug.py sets up logging


class SubclassPatcherUI(object):
    def setupUi(self, SubclassPatcherUI):
        try:
            # Main UI Setup
            SubclassPatcherUI.setObjectName("SubclassPatcherUI")
            SubclassPatcherUI.resize(600, 400)

            # Main Layout
            self.gridLayout_3 = QtWidgets.QGridLayout(SubclassPatcherUI)
            self.gridLayout_3.setObjectName("gridLayout_3")

            # List of Mods
            self.lstMods = QtWidgets.QListView(SubclassPatcherUI)
            self.lstMods.setObjectName("lstMods")
            self.gridLayout_3.addWidget(self.lstMods, 0, 0, 1, 1)

            # Secondary Grid Layout for Input Fields and Buttons
            self.gridLayout = QtWidgets.QGridLayout()
            self.gridLayout.setObjectName("gridLayout")

            # Line Edit Field
            self.lineEdit = QtWidgets.QLineEdit(SubclassPatcherUI)
            self.lineEdit.setObjectName("lineEdit")
            self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)

            # Push Button
            self.pushButton = QtWidgets.QPushButton(SubclassPatcherUI)
            self.pushButton.setObjectName("pushButton")
            self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)

            # Tool Button
            self.toolButton = QtWidgets.QToolButton(SubclassPatcherUI)
            self.toolButton.setObjectName("toolButton")
            self.gridLayout.addWidget(self.toolButton, 0, 1, 1, 1)

            # Adding Secondary Grid Layout to Main Layout
            self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)

            # Apply Translations and Connect Slots
            self.retranslateUi(SubclassPatcherUI)
            QtCore.QMetaObject.connectSlotsByName(SubclassPatcherUI)
        except Exception as e:
            logging.error(f"Error setting up UI: {e}")

    def retranslateUi(self, SubclassPatcherUI):
        try:
            _translate = QtCore.QCoreApplication.translate
            SubclassPatcherUI.setWindowTitle(_translate("SubclassPatcherUI", "BG3 Subclass Patcher"))
            self.pushButton.setText(_translate("SubclassPatcherUI", "Create Patch"))
            self.toolButton.setText(_translate("SubclassPatcherUI", "..."))
        except Exception as e:
            logging.error(f"Error translating UI: {e}")
