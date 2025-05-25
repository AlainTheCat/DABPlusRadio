# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'service.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QStatusBar, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(775, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(10, 10, 281, 23))
        self.progressBar.setMaximum(39)
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)
        self.labelScanning = QLabel(self.centralwidget)
        self.labelScanning.setObjectName(u"labelScanning")
        self.labelScanning.setGeometry(QRect(310, 10, 171, 17))
        self.labelNbServices = QLabel(self.centralwidget)
        self.labelNbServices.setObjectName(u"labelNbServices")
        self.labelNbServices.setGeometry(QRect(500, 10, 191, 17))
        self.lineEditNbServices = QLineEdit(self.centralwidget)
        self.lineEditNbServices.setObjectName(u"lineEditNbServices")
        self.lineEditNbServices.setGeometry(QRect(700, 10, 61, 25))
        self.lineEditNbServices.setAlignment(Qt.AlignCenter)
        self.tableWidgetService = QTableWidget(self.centralwidget)
        if (self.tableWidgetService.columnCount() < 5):
            self.tableWidgetService.setColumnCount(5)
        self.tableWidgetService.setObjectName(u"tableWidgetService")
        self.tableWidgetService.setGeometry(QRect(10, 40, 751, 451))
        self.tableWidgetService.setColumnCount(5)
        self.tableWidgetService.horizontalHeader().setVisible(True)
        self.tableWidgetService.horizontalHeader().setDefaultSectionSize(150)
        self.pushButtonClose = QPushButton(self.centralwidget)
        self.pushButtonClose.setObjectName(u"pushButtonClose")
        self.pushButtonClose.setGeometry(QRect(670, 520, 89, 25))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 775, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.labelScanning.setText(QCoreApplication.translate("MainWindow", u"Scanning ...", None))
        self.labelNbServices.setText(QCoreApplication.translate("MainWindow", u"Total number of services", None))
        self.lineEditNbServices.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.pushButtonClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))
    # retranslateUi

