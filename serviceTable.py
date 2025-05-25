#!/usr/bin/python3
# This Python file uses the following encoding: utf-8
# -*- coding: utf-8 -*-
"""
 DAB Radio receiver on USB HID

 This is a control panel of DAB radio receiver.
 This program is build with Python 3, PySide6 and QtDesigner.
 The device is plugged on USB HID.
 For installation read readme.txt file and requirements.txt.

 Author: Alain the Cat
 Local Website: mao2.fr
"""

import sys

from Table import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QMessageBox, QApplication, QTableWidget, QTableWidgetItem
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon, QColor, QPixmap

class TableService(QMainWindow, Ui_MainWindow):
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
        self.setWindowTitle("RADIO DAB SCANNING")

        self.my_array = [[0 for i in range(5)] for i in range(40)]

        self.index = 0
        self.totalServices = 0

        self.progressBar.setValue(0)
        self.loadTable()

        self.pushButtonClose.clicked.connect(self.close)

# GETTERS AND SETTERS
    def setArray(self, my_array):

        self.my_array = my_array
        self.loadTable()

    def setIndex(self, index):

        self.index = index
        self.progressBar.setValue(index)

    def setTotalServices(self, totalServices):

        self.totalServices = totalServices
        self.lineEditNbServices.setText(str(self.totalServices))

    def getArray(self):

        return self.my_array

    def getIndex(self):

        return self.index

    def getTotalServices(self):

        return self.totalServices

    def loadTable(self):

        # Table dimension
        rowCount = len(self.my_array)
        columnCount = len(self.my_array[0])
        self.tableWidgetService.setRowCount(rowCount)
        self.tableWidgetService.setColumnCount(columnCount)

        # Adding header to the table
        headerH = ['Tune Index', 'Freq. (Mhz)', 'RSSI (dBµV)', "Valid", "Nb Services"]
        self.tableWidgetService.setHorizontalHeaderLabels(headerH)

        # Adding a first row
        for row in range(rowCount):
            for col in range(columnCount):
                self.tableWidgetService.setItem(row, col, QTableWidgetItem(str(self.my_array[row][col])))



"""
    def main():

    app = QApplication(sys.argv)
    window = TableService()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
"""

