# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Form3.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QProgressBar, QSizePolicy, QStatusBar, QWidget)

class Ui_Form3(object):
    def setupUi(self, Form3):
        if not Form3.objectName():
            Form3.setObjectName(u"Form3")
        Form3.resize(318, 134)
        self.centralwidget = QWidget(Form3)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 20, 281, 17))
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(20, 50, 281, 23))
        self.progressBar.setValue(0)
        Form3.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Form3)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 318, 22))
        Form3.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Form3)
        self.statusbar.setObjectName(u"statusbar")
        Form3.setStatusBar(self.statusbar)

        self.retranslateUi(Form3)

        QMetaObject.connectSlotsByName(Form3)
    # setupUi

    def retranslateUi(self, Form3):
        Form3.setWindowTitle(QCoreApplication.translate("Form3", u"Tunning for a new ensemble", None))
        self.label.setText(QCoreApplication.translate("Form3", u"TextLabel", None))
    # retranslateUi

