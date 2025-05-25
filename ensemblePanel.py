#!/usr/bin/python3
# This Python file uses the following encoding: utf-8
# -*- coding: utf-8 -*-
"""
 DAB Radio receiver on USB HID

 This is a control panel of DAB radio receiver.
 This program is build with Python 3, PySide6 and QtDesigner.
 The device is plugged on USB HID.
 For installation read readme.txt file and requirements.txt.

 Author: Alain theCat
 Local Website: mao2.fr
"""

import sys

from ensemble import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QMessageBox, QApplication, QTableWidget, QTableWidgetItem
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon, QColor, QPixmap

class Ensemble(QMainWindow, Ui_MainWindow):
    """
    DAB Radio panel (creating and playing)
    """

    def __init__(self):
        """Initializes the MainWindow class"""
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setupUi(self)
        self.setWindowIcon(QIcon("radio.png"))
        self.setWindowTitle("TUNING")

        self.progressBar.setValue(0)

# GETTERS AND SETTERS
    def setProgressBarValue(self, value):

        self.value = value
        self.progressBar.setValue(self.value)

    def setLabel(self, label):

        self.label = label
        self.labelInfo.setText(self.label)

    def getProgressBarValue(self):

        return self.progressBar.value()



"""
    def main():

    app = QApplication(sys.argv)
    window = TableService()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
"""
