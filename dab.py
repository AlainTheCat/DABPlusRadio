#!/usr/bin/python3
# This Python file uses the following encoding: utf-8
# -*- coding: utf-8 -*-
"""
 DAB Radio receiver on USB HID

 Warning: This is a debug version

 This is a control panel of DAB radio receiver.
 This program is build with Python 3, PySide 6 and QtDesigner.
 The device is plugged on USB HID.
 The style is combinear.qss

 For installation read readme.txt file and requirements.txt.

 Author: Alain the Cat
 Local Website: mao2.fr
"""

import os
import platform
import sys
import hid
import json

from MainWindow import Ui_Form
from PySide6.QtWidgets import QMainWindow, QMessageBox, QApplication, QTableWidgetItem, QFileDialog, QInputDialog
from PySide6.QtCore import QTimer, QObject, Signal, QDate, QTime, QByteArray, QFile, QIODevice
from PySide6.QtGui import QIcon, QPixmap

from hid import HIDException
from qled import QLed
from serviceTable import TableService
from ensemblePanel import Ensemble
from preset import Preset
from service import Service
from constants import DLS_Ascii, VENDOR_ID, PRODUCT_ID
from localErrors import UsbHidIOError
from pathlib import Path

class Communicate(QObject):
    updateDisplay = Signal(int)

def checkDevice():
    """Checks the device on Linux or Windows platform."""
    if platform.system() == "Linux" or platform.system() == "Windows":
        try:
            device = hid.Device(vid=VENDOR_ID, pid=PRODUCT_ID)
            return device
        except HIDException as e:
            if platform.system() == "Linux":
                try:
                    res = hid.enumerate(vid=VENDOR_ID, pid=PRODUCT_ID)
                    dict1 = res[0]
                    hidPath = dict1["path"].decode()
                    msgBox1 = QMessageBox()
                    msgBox1.setWindowTitle("DEVICE ERROR")
                    msgBox1.setText("Permission denied")
                    msgBox1.setInformativeText("Plug your Device and give permission\n sudo chmod 0666 " + hidPath)
                    msgBox1.setStandardButtons(QMessageBox.StandardButton.Ok)
                    if msgBox1.exec() == QMessageBox.StandardButton.Ok:
                        exit()
                    else:
                        pass
                except HIDException as e:
                    msgBox3 = QMessageBox()
                    msgBox3.setWindowTitle("DEVICE ERROR")
                    msgBox3.setText("Device no found")
                    msgBox3.setInformativeText("Plug your device:" + e)
                    msgBox3.setStandardButtons(QMessageBox.StandardButton.Ok)
                    if msgBox3.exec() == QMessageBox.StandardButton.Ok:
                        exit()
                    else:
                        pass
            else:
                msgBox2 = QMessageBox()
                msgBox2.setWindowTitle("DEVICE ERROR")
                msgBox2.setText("Device no found")
                msgBox2.setInformativeText("Plug your device !")
                msgBox2.setStandardButtons(QMessageBox.StandardButton.Ok)
                if msgBox2.exec() == QMessageBox.StandardButton.Ok:
                    exit()
                else:
                    pass


def serviceListNotAvailable():
    """Displays in a popup that the service list is not available(case response is 0xFF)."""
    msgBox4 = QMessageBox()
    msgBox4.setWindowTitle("DAB ERROR")
    msgBox4.setText("Service List is not available !!!")
    msgBox4.setInformativeText("Check your antenna or start a new scan.")
    msgBox4.setStandardButtons(QMessageBox.StandardButton.Ok)
    if msgBox4.exec() == QMessageBox.StandardButton.Ok:
        pass
    else:
        pass


class Dab(QMainWindow, Ui_Form):
    """DAB Radio panel (creating and playing)"""

    def __init__(self):
        """Initializes the MainWindow class"""
        super().__init__()

        # ---INIT PANEL ---
        # Creating main window from dab.ui / dab.py
        self.setupUi(self)
        self.setWindowIcon(QIcon("radio.png"))
        self.setWindowTitle("RADIO DAB")

        # --- INIT SOME VARIABLE ---
        # Read and write buffers
        self.bufferIn = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        """
        IN -> Read from the Device
        Received data will be stored here - the first byte in the array is unused
        bufferInSize = 40  -> Size of the data buffer coming IN to the PC
        """
        self.bufferOut = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                          0x00]
        """
        OUT -> Write to the device
        Transmitted data is stored here - the first item in the array must be 0
        bufferOutSize = 16  -> Size of the data buffer going OUT from the PC
        """

        #  Creating list of services
        self.nbServices = 0
        self.services = []
        self.currentIndex = 0
        self.totalServices = 0
        self.tuneIndex = 0
        self.rowPosition = 0
        self.currentTuneIndex = 0
        self.currentTuneFrequency = 0
        self.currentEID = 0x00
        self.currentComponentLabel = ""

        #  Creating list of presets
        self.nbPresets = 0
        self.presets = []

        self.hidToSend = False

        # Init Status Bar
        self.dynamicLabel = "Alain is - the best"
        self.artist = ""
        self.title = ""

        self.packetIndex = 0
        self.PADDataType = 0
        self.DLSType = 0
        self.MOTSLSType = 0
        self.DLSLength = 0
        self.SLSLength = 0
        self.payloadLength = 0

        self.jackStatus = 0x00
        """Analog or Optical output"""
        self.labelVolume = "0"

        # Init Picture
        self.imageStart = False
        """Beginning for load the picture""" 
        self.pathPicture = ""
        """Path of the picture"""
        self.pictureByte = QByteArray()
        """Content of the picture in Byte format"""
        self.pictureFile = "picture.jpg"
        """Picture name for init"""
        self.pictureResult = []
        """Content array of the picture"""
        self.fileJPG = QFile
        """File for load Image"""
        self.saveImage = False

        # --- INIT DEVICE ---
        self.myDevice = checkDevice()

        # --- INIT SOME WIDGET ---
        self.pushButtonOn.setEnabled(True)
        self.pushButtonOff.setEnabled(False)
        self.pushButtonScan.setEnabled(False)
        self.checkBoxMute.setEnabled(False)
        self.checkBoxMono.setEnabled(False)
        self.checkBoxArtistTitle.setEnabled(False)
        self.tableWidgetViewServices.setEnabled(False)
        self.pushButtonSaveList.setEnabled(False)
        self.horizontalScrollBarVolume.setEnabled(False)
        self.checkBoxSaveImage.setEnabled(False)
        self.presetsButtonDisabled()

        self.toolStripStatusLabel1.setText("DAB Tuner not connected")
        self.toolStripStatusLabel2.setText("")
        self.toolStripStatusLabel3.setText("")
        self.toolStripStatusLabel4.setText("")

        self.bufferAddress = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10, 0x11, 0x012,
                              0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25,
                              0x26, 0x27, 0x28, 0x29, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38,
                              0x39]

        self.dataAddress = ' '.join('{:02X}'.format(a) for a in self.bufferAddress)
        self.lineEditAddress.setText(self.dataAddress)

        self.led = QLed()
        self.layoutPower.insertWidget(0, self.led)

        self.image = QPixmap()

        self.service = TableService()

        self.ensemble = Ensemble()
        # For scanning, create a tab :
        # row -> tune index
        # column -> 0: tune index, 1: frequency, 2: RSSI, 3: valid, 4: nb services
        self.my_array = [[0 for col in range(5)] for row in range(41)]
        headerH = ['Preset','Service Name', 'Service ID', 'Component ID', 'Tune Index', 'Tune Frequency kHz', 'EID',
                   'Component Label', ]
        self.tableWidgetViewServices.setHorizontalHeaderLabels(headerH)

        # --- INIT CONNECTIONS ---
        self.pushButtonOn.clicked.connect(self.on)
        self.pushButtonOff.clicked.connect(self.off)
        self.pushButtonScan.clicked.connect(self.buttonScanClick)

        self.horizontalScrollBarVolume.valueChanged.connect(self.hScrollBarVolumeValueChanged)

        self.tableWidgetViewServices.clicked.connect(self.dataGridViewServicesCellClick)

        self.checkBoxMono.clicked.connect(self.checkBoxMonoClick)
        self.checkBoxMute.clicked.connect(self.checkBoxMuteClick)

        self.comboBoxAreas.addItems(["Default Area"])
        self.comboBoxAreas.setCurrentText("Default Area")

        self.checkBoxSaveImage.clicked.connect(self.saveImageEnable)

        self.memory = False
        self.pushButtonMemory.clicked.connect(self.buttonMemoryClick)

        # Find the different Services list (json files in json directory)
        # and add this services list in Areas comboBx
        self.getServicesFile()
        self.pushButtonSaveList.clicked.connect(self.saveServicesList)

        # --- PUSH BUTTON PRESETS ---

        self.pushButtonPreset1.clicked.connect(lambda: self.buttonPresetClick(0))
        self.pushButtonPreset2.clicked.connect(lambda: self.buttonPresetClick(1))
        self.pushButtonPreset3.clicked.connect(lambda: self.buttonPresetClick(2))
        self.pushButtonPreset4.clicked.connect(lambda: self.buttonPresetClick(3))
        self.pushButtonPreset5.clicked.connect(lambda: self.buttonPresetClick(4))
        self.pushButtonPreset6.clicked.connect(lambda: self.buttonPresetClick(5))
        self.pushButtonPreset7.clicked.connect(lambda: self.buttonPresetClick(6))
        self.pushButtonPreset8.clicked.connect(lambda: self.buttonPresetClick(7))
        self.pushButtonPreset9.clicked.connect(lambda: self.buttonPresetClick(8))
        self.pushButtonPreset10.clicked.connect(lambda: self.buttonPresetClick(9))
        self.pushButtonPreset11.clicked.connect(lambda: self.buttonPresetClick(10))
        self.pushButtonPreset12.clicked.connect(lambda: self.buttonPresetClick(11))

        # --- CHECK SOME FUNCTION
        # self.pushButtonTest4.clicked.connect(self.timer4Tick)

        self.com = Communicate()

        # --- INIT TIMERS ---
        # Power Up -> delay one shot 100 mSec
        self.timerPowerUp = QTimer()
        self.timerPowerUp.setSingleShot(True)
        self.timerPowerUp.timeout.connect(self.open)

        # Power Down -> delay one shot 50 mSec
        self.timerPowerDown = QTimer()
        self.timerPowerDown.setSingleShot(True)
        self.timerPowerDown.timeout.connect(self.off)

        # Artist Title -> delay one shot 100 mSec
        self.timerArtistTitle = QTimer()
        self.timerArtistTitle.setSingleShot(True)
        # self.timerArtistTitle.timeout.connect(self.timerArtistTitleTick)

        # New Ensemble -> delay one shot 300 mSec
        self.timerNewEnsemble = QTimer()
        self.timerNewEnsemble.setSingleShot(True)
        self.timerNewEnsemble.timeout.connect(self.timerNewEnsembleTick())

        # Read device -> periodic delay 50 mSec
        self.timerReadDevice = QTimer()
        self.timerReadDevice.timeout.connect(self.readDevice)

        # HID to send -> delay 50 mSec
        # self.timerHidToSend = QTimer()
        # self.timerHidToSend.timeout.connect(self.timerHidToSendTick())


    def off(self):
        """Power Off"""
        self.led.toggleValue()
        self.toolStripStatusLabel1.setText("DAB Tuner Disconnected")
        self.toolStripStatusLabel2.setText("")
        self.toolStripStatusLabel3.setText("")
        self.toolStripStatusLabel4.setText("")
        self.pushButtonOn.setEnabled(True)
        self.pushButtonOff.setEnabled(False)
        self.comboBoxAreas.setEnabled(True)
        self.tableWidgetViewServices.setEnabled(False)
        self.presetsButtonDisabled()
        self.clearPanel()
        self.clearTextBox()

    def close(self):
        """Closes the device (Stand by)."""
        # self.timerPowerDown.stop()
        self.horizontalScrollBarVolume.setValue(0)
        self.bufferOut[0] = 0x00
        self.bufferOut[1] = 0x00  # Stand by the device ( stop the HID coming IN to the PC )
        # self.hidToSend = True
        self.hidSend()
        self.timerPowerDown.start(50) # Power off after 50ms delay

    def clearPanel(self):
        """Clears this panel."""
        self.labelRSSI.setText("0 db V")
        self.labelSNR.setText("0 dB")
        self.labelCNR.setText("0 dB")
        self.labelFIC.setText("0")
        self.checkBoxMono.setEnabled(False)
        self.checkBoxMute.setEnabled(False)
        self.checkBoxSaveImage.setEnabled(False)
        self.horizontalScrollBarVolume.setEnabled(False)

    def clearTextBox(self):
        """Clears all TextBox (lineEdit)"""
        self.lineEditCurrentService.setText("")
        self.lineEditArtistDLS.setText("")
        self.lineEditTitle.setText("")
        self.lineEditBufferIn.setText("")
        self.lineEditBufferOut.setText("")
        self.lineEditPacket.setText("")
        self.lineEditPictureName.setText("")
        self.lineEditDateTime.setText("")

    def on(self):
        """Power On"""
        # Load Services list from selected json file in Area SpinBox
        # and prohibit changing the services list
        self.loadServiceList()
        self.comboBoxAreas.setEnabled(False)

        # Load Presets list from Services list with position mark ("1" to "12")
        self.loadPresets()

        # Update Status Bar
        self.toolStripStatusLabel1.setText("DAB Tuner connected")
        self.toolStripStatusLabel2.setText("")
        self.toolStripStatusLabel3.setText("")
        self.toolStripStatusLabel4.setText("")

        # Swap buttons On/Off
        self.pushButtonOn.setEnabled(False)
        self.pushButtonOff.setEnabled(True)

        # Some Buttons are now enabled
        self.horizontalScrollBarVolume.setEnabled(True)
        self.checkBoxMono.setEnabled(True)
        self.checkBoxMute.setEnabled(True)
        self.checkBoxArtistTitle.setEnabled(True)
        self.checkBoxSaveImage.setEnabled(True)
        self.pushButtonScan.setEnabled(True)
        self.pushButtonSaveList.setEnabled(True)

        # light on the LED
        self.led.toggleValue()

        self.timerPowerUp.start(100)    # Sends the open command after a 100 ms delay

    def open(self):
        """Opens the device. A HID device has been plugged in..."""
        # self.timerPowerUp.stop()
        self.bufferOut[0] = 0x00
        self.bufferOut[1] = 0x01
        self.bufferOut[2] = 0x02
        self.bufferOut[3] = 0x00
        self.bufferOut[4] = 0x00
        self.bufferOut[5] = 0x09
        self.bufferOut[6] = 0xF2
        self.bufferOut[7] = 0x00
        self.bufferOut[8] = 0x00
        self.bufferOut[9] = 0x00
        self.bufferOut[10] = 0x00
        self.bufferOut[11] = 0x00
        self.bufferOut[12] = 0x00
        self.bufferOut[13] = 0x00
        self.bufferOut[14] = 0x00
        self.bufferOut[15] = 0x00
        # self.hidToSend = True
        self.hidSend()
        self.timerReadDevice.start(10)  # Reads the device every 50ms

    def getServicesFile(self):
        """Gets number of file services json and name of this file and updates the Areas comboBox"""
        directory = "json"
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        for row in range(1,len(files)):
            item = files[row].replace("services-", "").replace(".json", "")
            self.comboBoxAreas.addItems([item])

    def loadServiceList(self):
        """Loads the Services List."""
        index = self.comboBoxAreas.currentIndex()
        if index == 0 :
            serviceList = "json/services-Default.json"
        else:
            serviceList = "json/services-"+ self.comboBoxAreas.currentText() + ".json"

        # List all services from json file
        with open(serviceList, "r", encoding="utf-8") as f:
            data1 = json.load(f)

        self.nbServices = sum([1 for i in data1])

        self.services.clear()
        # Appending instances to list
        for i in range(1, self.nbServices + 1):
            self.services.append(
                Service(
                    data1["service" + str(i)]["Preset"],
                    data1["service" + str(i)]["Service Name"],
                    data1["service" + str(i)]["Service ID"],
                    data1["service" + str(i)]["Component ID"],
                    data1["service" + str(i)]["Tune Index"],
                    data1["service" + str(i)]["Tune Frequency kHz"],
                    data1["service" + str(i)]["EID"],
                    data1["service" + str(i)]["Component Label"]
                )
            )
        self.tableWidgetViewServices.clearContents() # Clear the table of services
        if self.nbServices != 0 :
            for row in range(0, self.nbServices):
                self.tableWidgetViewServices.setItem(row, 0, QTableWidgetItem(self.services[row].preset))
                self.tableWidgetViewServices.setItem(row, 1, QTableWidgetItem(self.services[row].serviceName))
                self.tableWidgetViewServices.setItem(row, 2, QTableWidgetItem(self.services[row].serviceID))
                self.tableWidgetViewServices.setItem(row, 3, QTableWidgetItem(self.services[row].componentID))
                self.tableWidgetViewServices.setItem(row, 4, QTableWidgetItem(self.services[row].tuneIndex))
                self.tableWidgetViewServices.setItem(row, 5, QTableWidgetItem(self.services[row].tuneFrequency))
                self.tableWidgetViewServices.setItem(row, 6, QTableWidgetItem(self.services[row].EID))
                self.tableWidgetViewServices.setItem(row, 7, QTableWidgetItem(self.services[row].componentLabel))
            self.lineEditArtistDLS.setText("Select a Service from the list")

            # Load all presets
            self.nbPresets = 0
            self.presets.clear()

            for index in range(1, 13):
                for row in range(0, self.nbServices):
                    if self.services[row].preset == str(index):
                        self.presets.append(
                            Preset(
                                str(row),
                                self.services[row].serviceName,
                                self.services[row].serviceID,
                                self.services[row].componentID,
                                self.services[row].tuneIndex,
                                self.services[row].tuneFrequency,
                                self.services[row].EID,
                                self.services[row].componentLabel
                            )
                        )
            self.nbPresets = len(self.presets)
            self.loadPresets()
        else :
            msgBox5 = QMessageBox()
            msgBox5.setWindowTitle("DAB WARNING")
            msgBox5.setText("Services list is empty : scan for services")
            msgBox5.setStandardButtons(QMessageBox.StandardButton.Ok)
            if msgBox5.exec() == QMessageBox.StandardButton.Ok:
                pass
            else:
                pass

    def loadServiceListAfterScan(self):
        """Loads Service List  after scan"""
        self.tableWidgetViewServices.clearContents()  # Clear the table of services
        if self.nbServices != 0:
            for row in range(0, self.nbServices):
                self.tableWidgetViewServices.setItem(row, 0, QTableWidgetItem(self.services[row].preset))
                self.tableWidgetViewServices.setItem(row, 1, QTableWidgetItem(self.services[row].serviceName))
                self.tableWidgetViewServices.setItem(row, 2, QTableWidgetItem(self.services[row].serviceID))
                self.tableWidgetViewServices.setItem(row, 3, QTableWidgetItem(self.services[row].componentID))
                self.tableWidgetViewServices.setItem(row, 4, QTableWidgetItem(self.services[row].tuneIndex))
                self.tableWidgetViewServices.setItem(row, 5, QTableWidgetItem(self.services[row].tuneFrequency))
                self.tableWidgetViewServices.setItem(row, 6, QTableWidgetItem(self.services[row].EID))
                self.tableWidgetViewServices.setItem(row, 7, QTableWidgetItem(self.services[row].componentLabel))
            self.lineEditArtistDLS.setText("Select a Service from the list")

    def readDevice(self):
        """Reads the device"""
        # self.timer.stop()
        try:
            self.bufferIn = self.myDevice.read(size=40, timeout=1)
            if self.bufferIn:
                dataInHex = ' '.join('{:02X}'.format(a) for a in self.bufferIn)
                self.lineEditBufferIn.setText(dataInHex)
                self.onRead()
        except UsbHidIOError:
            pass
            # msgBox = QMessageBox()
            # msgBox.setWindowTitle("Message")
            # msgBox.setText("Reading error")
            # msgBox.setStandardButtons(QMessageBox.StandardButton.Cancel)
            # msgBox.setDefaultButton(QMessageBox.StandardButton.Cancel)
            # answer = msgBox.exec()
            # if answer == QMessageBox.StandardButton.Cancel:
            #     pass

    def onRead(self):
        """Reads bytes in bufferIn from the microcontroller and determines which function to run.
        These bytes come after 50 ms interval maximum.
        """
        # self.timerHidToSend.start(50)

        match self.bufferIn[0]:
            case 0x08:                # Response 0x08 GET_PART_INFO ( See AN649 )
                self.partInfo()
            case 0x09:               # Response 0x09 GET_SYS_STATE ( See AN649 )
                self.systemState()
            case 0x12:               # Response 0x12 GET_FUNC_INFO ( See AN649 )
                self.firmwareRevision()
            case 0x80:               # Response 0x80 GET_DIGITAL_SERVICE_LIST ( See AN649 )
                self.digitalServiceList()
            case 0x84:               # Response 0x84. GET_DIGITAL_SERVICE_DATA ( See AN649 )
                self.getDigitalServiceData()
            case 0xB2:               # Response 0xB2 DAB_DIGRAD_STATUS ( See AN649 )
                self.dabDigradStatus()
            case 0xB4:               # Response 0xB4 DAB_GET_ENSEMBLE_INFO ( See AN649 )
                self.ensembleInfo()
            case 0xBC:               # Response 0xBC DAB_GET_TIME ( See AN649 )
                self.dabGetTime()
            case 0xBD:               # Response 0xBD DAB_GET_AUDIO_INFO ( See AN649 )
                self.dabGetAudioInfo()
            case 0xC0:               # Response 0xC0 DAB_GET_SERVICE_INFO ( See AN649 )
                self.dabGetServiceInfo()
            case 0xF0:               # Tuning for a new ensemble
                self.tuningForNewEnsemble()
            case 0xFF:               # Service List not available
                serviceListNotAvailable()

    def partInfo(self):
        """Provides the Part Info (Skyworks and Microchip numbers)."""
        Skyworks_Part_Number = str(self.bufferIn[13] * 256 + self.bufferIn[12])
        Microchip_Part_Number = chr(self.bufferIn[27]) + chr(self.bufferIn[28]) + chr(self.bufferIn[29]) + \
                                chr(self.bufferIn[30]) + chr(self.bufferIn[31]) + chr(self.bufferIn[32]) + \
                                chr(self.bufferIn[33]) + chr(self.bufferIn[34]) + chr(self.bufferIn[35]) + \
                                chr(self.bufferIn[36]) + chr(self.bufferIn[37]) + chr(self.bufferIn[38])
        partInfoText = Microchip_Part_Number + " / Si" + Skyworks_Part_Number
        self.toolStripStatusLabel2.setText(partInfoText)

    def systemState(self):
        """Analyzes the states of the system.
        """
        productName = chr(self.bufferIn[10]) + chr(self.bufferIn[11]) + chr(self.bufferIn[12]) + \
                        chr(self.bufferIn[13]) + chr(self.bufferIn[14]) + chr(self.bufferIn[15]) + \
                        chr(self.bufferIn[16]) + chr(self.bufferIn[17]) + chr(self.bufferIn[18]) + \
                        chr(self.bufferIn[19]) + chr(self.bufferIn[20]) + chr(self.bufferIn[21]) + \
                        chr(self.bufferIn[22]) + chr(self.bufferIn[23]) + chr(self.bufferIn[24]) + \
                        chr(self.bufferIn[25]) + chr(self.bufferIn[26]) + chr(self.bufferIn[27]) + \
                        chr(self.bufferIn[28]) + chr(self.bufferIn[29]) + chr(self.bufferIn[30]) + \
                        chr(self.bufferIn[31]) + chr(self.bufferIn[32]) + chr(self.bufferIn[33]) + \
                        chr(self.bufferIn[34]) + chr(self.bufferIn[35]) + chr(self.bufferIn[36]) + \
                        chr(self.bufferIn[37]) + chr(self.bufferIn[39]) + chr(self.bufferIn[39])
        self.toolStripStatusLabel1.setText(productName + "Connected")

        Image_System = self.bufferIn[8]
        match Image_System:
            case 0:
                self.toolStripStatusLabel3.setText("Bootloader is active")
            case 1:
                self.toolStripStatusLabel3.setText("FMHD is active")
            case 2:
                self.volume()
                self.toolStripStatusLabel3.setText("DAB is active")
                # self.presetsButtonEnabled()
                self.pushButtonScan.setEnabled(True)
                self.checkBoxMute.setEnabled(True)
                self.checkBoxMono.setEnabled(True)
                self.checkBoxArtistTitle.setEnabled(True)
                self.tableWidgetViewServices.setEnabled(True)
                self.horizontalScrollBarVolume.setEnabled(True)
                # self.lineEditArtistDLS.setText("Select a Service from the list")

                # Load the Default Image ( 320x240 )
                pixmap = QPixmap("DAB_Default.jpg")
                self.labelPicture.setPixmap(pixmap)
                # Another
                for x in range(16):
                    self.bufferOut[x] = 0x00
                self.bufferOut[1] = 0x13    # Modify this property here to enable another PAD
                self.bufferOut[4] = 0xB4    # Property 0xB400. DAB_XPAD_ENABLE ( See AN649 )
                self.bufferOut[5] = 0x05    # 0x0005 : DLS and MOT SLS are enabled by default
                self.hidToSend = True

            case 3:
                self.toolStripStatusLabel3.setText("TDMB or data only DAB image is active")
            case 4:
                self.toolStripStatusLabel3.setText("FMHD Demod is active")
            case 5:
                self.toolStripStatusLabel3.setText("AMHD is active")
            case 6:
                self.toolStripStatusLabel3.setText("AMHD Demod is active")
            case 7:
                self.toolStripStatusLabel3.setText("FMHD is active")
            case 9:
                self.toolStripStatusLabel3.setText("DAB Demod is active")

    def firmwareRevision(self):
        """Provides the SI firmware and PIC firmware"""
        SI_First_Rev = str(self.bufferIn[8])
        SI_Second_Rev = str(self.bufferIn[9])
        SI_Third_Rev = str(self.bufferIn[10])
        PIC_First_Rev = str(self.bufferIn[16])
        PIC_Second_Rev = str(self.bufferIn[17])
        PIC_Third_Rev = str(self.bufferIn[18])
        firmwareText = " PIC Firmware revision : " + PIC_First_Rev + "." + PIC_Second_Rev + "." + PIC_Third_Rev + \
                       " / Si Firmware revision : " + SI_First_Rev + "." + SI_Second_Rev + "." + SI_Third_Rev
        self.toolStripStatusLabel4.setText(firmwareText)

    def digitalServiceList(self):
        """Provides the Digital Service List"""
        serviceID = hex(self.bufferIn[15] * 16777216 + self.bufferIn[14] * 65536 + self.bufferIn[13] * 256 + self.bufferIn[12])
        serviceName = ""
        for index in range(20, 36):
            serviceName = serviceName + chr(DLS_Ascii[self.bufferIn[index]])
        componentID = hex(self.bufferIn[39] * 16777216 + self.bufferIn[38] * 65536 + self.bufferIn[37] * 256 + self.bufferIn[36])
        if self.bufferOut[1] == 0x40:
            self.nbServices += 1
            self.totalServices += 1
            self.my_array[self.currentTuneIndex][4] = self.nbServices
            self.service.lineEditNbServices.setText(str(self.totalServices))
        self.tableWidgetViewServices.insertRow(self.rowPosition)
        self.tableWidgetViewServices.setItem(self.rowPosition, 0, QTableWidgetItem("0"))
        self.tableWidgetViewServices.setItem(self.rowPosition, 1, QTableWidgetItem(serviceName))
        self.tableWidgetViewServices.setItem(self.rowPosition, 2, QTableWidgetItem(serviceID))
        self.tableWidgetViewServices.setItem(self.rowPosition, 3, QTableWidgetItem(componentID))
        self.tableWidgetViewServices.setItem(self.rowPosition, 4, QTableWidgetItem(str(self.currentTuneIndex)))
        self.tableWidgetViewServices.setItem(self.rowPosition, 5, QTableWidgetItem(str(self.currentTuneFrequency)))
        self.tableWidgetViewServices.setItem(self.rowPosition, 6, QTableWidgetItem(self.currentEID))
        self.tableWidgetViewServices.setItem(self.rowPosition, 7, QTableWidgetItem(self.currentComponentLabel))

        self. rowPosition = self. rowPosition + 1

    def readTableService(self, table):
        """
        Reads QTableWidget and return a dictionary of contents
        :param table: Tables of services
        """
        content = {}
        nbRow = self.tableWidgetViewServices.rowCount()
        print("Total Services 2: ", self.tableWidgetViewServices.rowCount())
        for row in range(nbRow):
            key = "service" + str(row + 1)
            service = {}
            for column in range(table.columnCount()):
                header = table.horizontalHeaderItem(column).text()
                item = table.item(row, column).text() if table.item(row, column) else ""
                service[header] = item
            content[key] = service
        return content

    def saveServicesList(self):
        """Saves the services list into a new area json file"""
        area, ok = QInputDialog.getText(self , "Services List Save", "Enter the name of this area: ")
        if ok and area:
            fileName = "json/services-" + area.capitalize() + ".json"
            content = self.readTableService(self.tableWidgetViewServices)
            with open(fileName, "w", encoding='utf-8') as file:
                file.write(json.dumps(content, indent=4))
        else:
            pass

    def dabDigradStatus(self):
        """Provides the DAB Digrad Status"""
        # Tune frequency and index
        self.currentTuneFrequency = (self.bufferIn[19] * 0x1000000) + (self.bufferIn[18] * 0x10000) + (self.bufferIn[17] * 0x100) + self.bufferIn[16]
        self.currentTuneIndex = self.bufferIn[20]
        self.my_array[self.currentTuneIndex][0] = self.currentTuneIndex
        self.my_array[self.currentTuneIndex][1] = self.currentTuneFrequency

        # Analog or optical output
        if self.bufferIn[27] != self.jackStatus:
            self. jackStatus = self.bufferIn[27]
            match self.jackStatus:
                case 0x00:
                    self.labelOuput.setText("Analog Output")
                    self.horizontalScrollBarVolume.setEnabled(True)
                    self.labelVolume = self.horizontalScrollBarVolume.value().toString()
                    self.checkBoxMono.setEnabled(True)
                    self.checkBoxMute.setEnabled(True)
                case 0x02:
                    self.labelOuput.setText("Optical Output")
                    self.horizontalScrollBarVolume.setEnabled(False)
                    self.labelVolume = "0"
                    self.checkBoxMono.setEnabled(False)
                    self.checkBoxMute.setEnabled(True)
                case 0x03:
                    self.labelOuput.setText("")
                    self.horizontalScrollBarVolume.setEnabled(False)
                    self.labelVolume = "0"
                    self.checkBoxMono.setEnabled(False)
                    self.checkBoxMute.setEnabled(False)

        if self.bufferIn[10] < 128:
            RSSI = self.bufferIn[10] & 0x3F
        else:
            RSSI = self.bufferIn[10] - 256
        self.my_array[self.currentTuneIndex][2] = RSSI
        valid = self.bufferIn[9] & 0x01
        self.my_array[self.currentTuneIndex][3] = valid
        SNR = self.bufferIn[11]
        CNR = self.bufferIn[13]
        FICQuality = self.bufferIn[12]
        self.nbServices = 0
        if self.bufferOut[1] != 0x40:
            self.labelRSSI.setText(str(RSSI) + " dB V")
            self.progressBarRSSI.setValue(RSSI)
            self.labelSNR.setText(str(SNR) + " dB")
            if SNR > 20:
                self.progressBarSNR.setValue(20)
            else:
                self.progressBarSNR.setValue(SNR)
            self.labelCNR.setText(str(CNR) + " dB")
            if CNR > 54 :
                self.progressBarCNR.setValue(54)
            else:
                self.progressBarCNR.setValue(CNR)
            self.labelFIC.setText(str(FICQuality))
            if FICQuality > 100 :
                self.progressBarFIC.setValue(100)
            else:
                self.progressBarFIC.setValue(FICQuality)
        self.service.setArray(self.my_array)

        if self.bufferOut[1] == 0x40:
            self.service.progressBar.setValue(self.currentTuneIndex)
            self.service.labelScanning.setText("Scanning: " + str(self.currentTuneFrequency) + " Mhz")
            if self.currentTuneIndex == 39:
                self.service.labelScanning.setText("Scanning complete")
                self.service.pushButtonClose.setEnabled(True)
                if self.totalServices != 0:
                    self.lineEditArtistDLS.setText("Select a Service from the list")
                    self.nbServices = self.totalServices
                else:
                    self.lineEditArtistDLS.setText("No available service")

    def ensembleInfo(self):
        """Provides the Ensemble Information"""
        self.currentEID = hex(self.bufferIn[8] * 256  + self.bufferIn[9])
        self.currentComponentLabel = ""
        for index in range(10, 26):
            self.currentComponentLabel = self.currentComponentLabel + chr(DLS_Ascii[self.bufferIn[index]])
        # self.currentComponentLabel = chr(self.bufferIn[10]) + chr(self.bufferIn[11]) + chr(self.bufferIn[12]) \
        #                  + chr(self.bufferIn[13]) + chr(self.bufferIn[14]) + chr(self.bufferIn[15]) \
        #                  + chr(self.bufferIn[16]) + chr(self.bufferIn[17]) + chr(self.bufferIn[18]) \
        #                  + chr(self.bufferIn[19]) + chr(self.bufferIn[20]) + chr(self.bufferIn[21]) \
        #                  + chr(self.bufferIn[22]) + chr(self.bufferIn[23]) + chr(self.bufferIn[24]) \
        #                  + chr(self.bufferIn[25])
        # print("Component Label: ",self.currentComponentLabel)

    def getDigitalServiceData(self):
        """Provides the Digital Service Data"""
        pictureName = ""
        self.packetIndex = self.bufferIn[6]
        if self.packetIndex == 0x00:
            self.PADDataType = self.bufferIn[11]
            match self.PADDataType:
                case 0x80:  # DLS
                    self.DLSType = self.bufferIn[28]
                    self.DLSLength = self.bufferIn[22] - 3
                    # print("DLSLength: ", '{:02X}'.format(self.DLSLength))
                    match self.DLSType:
                        case 0x00:  #  New DLS
                            self.lineEditArtistDLS.setText("")
                            self.lineEditTitle.setText("")
                            self.dynamicLabel = ""
                            if self.DLSLength > 9:
                                for var in range(30, 40):
                                    # Char  , , , , ,...OK ( &H7F to &HFF )
                                    self.dynamicLabel = self.dynamicLabel + chr(DLS_Ascii[self.bufferIn[var]])
                                self.DLSLength = self.DLSLength - 10
                            else:
                                for var in range(30, self.DLSLength + 30):
                                    # Char  , , , , ,...OK ( &H7F to &HFF )
                                    self.dynamicLabel = self.dynamicLabel + chr(DLS_Ascii[self.bufferIn[var]])
                            # self.timerArtistTitle.setInterval(100)
                            self.timerArtistTitle.start()
                        case 0x80:  # New DLS
                            self.lineEditArtistDLS.setText("")
                            self.lineEditTitle.setText("")
                            self.dynamicLabel = ""
                            if self.DLSLength > 9:
                                for var in range(30, 40):
                                    # Char  , , , , ,...OK ( &H7F to &HFF )
                                    self.dynamicLabel = self.dynamicLabel + chr(DLS_Ascii[self.bufferIn[var]])
                                self.DLSLength = self.DLSLength - 10
                            else:
                                for var in range(30, self.DLSLength + 30):
                                    # Char  , , , , ,...OK ( &H7F to &HFF )
                                    self.dynamicLabel = self.dynamicLabel + chr(DLS_Ascii[self.bufferIn[var]])
                            # self.timerArtistTitle.setInterval(100)
                            self.timerArtistTitle.start()
                        case 0x12:
                            # print("Case: ", 0x12)
                            if self.bufferIn[33] != 0x0 and self.bufferIn[35] != 0x0 and self.bufferIn[36] != 0x0:
                                titleLen = self.bufferIn[33] + 1
                                artistLen = self.bufferIn[36] + 1
                                artistIndex = self.bufferIn[35]
                                self.title = self.dynamicLabel[0: titleLen]
                                self.artist = self.dynamicLabel[artistIndex: (artistIndex + artistLen)]
                                self.lineEditTitle.setText("Title: " + self.title)
                                self.lineEditArtistDLS.setText("Artist: " + self.artist)
                            else:
                                if self.checkBoxArtistTitle.isChecked():
                                    self.softLabelsArtistTitle()
                                else:
                                    self.lineEditArtistDLS.setText(self.dynamicLabel)
                        case 0x92:
                            if self.bufferIn[33] != 0x0 and self.bufferIn[35] != 0x0 and self.bufferIn[36] != 0x0:
                                titleLen = self.bufferIn[33] + 1
                                artistLen = self.bufferIn[36] + 1
                                artistIndex = self.bufferIn[35]
                                self.title = self.dynamicLabel[0: titleLen]
                                self.artist = self.dynamicLabel[artistIndex: (artistIndex + artistLen)]
                                self.lineEditTitle.setText("Title: " + self.title)
                                self.lineEditArtistDLS.setText("Artist: " + self.artist)
                            else:
                                if self.checkBoxArtistTitle.isChecked():
                                    self.softLabelsArtistTitle()
                                else:
                                    self.lineEditArtistDLS.setText(self.dynamicLabel)

                case 0x7C:
                    self.MOTSLSType = self.bufferIn[28]  # MOT SLS
                    self.SLSLength = self.bufferIn[35] * 256 + self.bufferIn[36]
                    match self.MOTSLSType:
                        case 0x73:  # Image Name
                            self.lineEditPictureName.setText("")
                        case 0x74:  # Image
                            result = []
                            indexImage = 0
                            if self.imageStart: # TRUE
                                indexImage = self.bufferIn[31] + 1
                                self.lineEditPacket.setText(str(indexImage))
                                for k in range(37, 40):
                                    result.append(self.bufferIn[k])
                                self.pictureByte = self.pictureByte.append(bytes(result))
                                self.SLSLength = self.SLSLength - 3
        else:
            self.payloadLength = self.bufferIn[7]
            match self.PADDataType:
                case 0x80:
                    if self.payloadLength > 1:
                        match self.DLSType:
                            case 0x00:
                                if self.DLSLength > 32:
                                    for var in range(8, 40):
                                        self.dynamicLabel = self.dynamicLabel + chr(DLS_Ascii[self.bufferIn[var]])
                                    self.DLSLength = self.DLSLength - 32
                                else:
                                    for var in range(8, self.DLSLength + 8):
                                        self.dynamicLabel = self.dynamicLabel + chr(DLS_Ascii[self.bufferIn[var]])
                            case 0x80:
                                if self.DLSLength > 32:
                                    for var in range(8, 40):
                                        self.dynamicLabel = self.dynamicLabel + chr(DLS_Ascii[self.bufferIn[var]])
                                    self.DLSLength = self.DLSLength - 32
                                else:
                                    for var in range(8, self.DLSLength + 8):
                                        self.dynamicLabel = self.dynamicLabel + chr(DLS_Ascii[self.bufferIn[var]])
                case 0x7C:
                    if self.payloadLength > 2:
                        match self.MOTSLSType:
                            case 0x73:
                                for var in range(20, 28):
                                    pictureName = pictureName + chr(DLS_Ascii[self.bufferIn[var]])
                                self.lineEditPictureName.setText(pictureName)
                                if pictureName != "":
                                    if self.saveImage:
                                        self.pictureFile = pictureName
                                        self.labelSavedImage.setText("* The last saved image: " + pictureName + " *")
                                    else:
                                        self.pictureFile = "picture.jpg"
                                    self.loadingPicture3()
                                self.imageStart = True
                            case 0x74:
                                if self.imageStart:
                                    result = []
                                    if self.SLSLength > 32:
                                        for k in range(8, 40):
                                            result.append(self.bufferIn[k])
                                        self.pictureByte = self.pictureByte.append(bytes(result))
                                        self.SLSLength = self.SLSLength - 32
                                    else:
                                        for k in range(8, self.SLSLength + 8):
                                            result.append(self.bufferIn[k])
                                        self.pictureByte = self.pictureByte.append(bytes(result))

    def timerArtistTitleTick(self):
        """Timer Artist Title Tick"""
        self.timerArtistTitle.stop()
        if self.checkBoxArtistTitle.isChecked():
            self.softLabelsArtistTitle()
        else:
            self.lineEditArtistDLS.setText(self.dynamicLabel)

    def softLabelsArtistTitle(self):
        """Displays the labels artist title."""
        dlsLen = len(self.dynamicLabel)
        charPosition = self.dynamicLabel.find(" - ", 0, dlsLen)
        if charPosition != 0:
            self.title = self.dynamicLabel[0: charPosition]
            self.artist = self.dynamicLabel[charPosition + 2: dlsLen]
            self.lineEditArtistDLS.setText(self.artist)
            self.lineEditTitle.setText(self.title)
        else:
            self.lineEditArtistDLS.setText(self.dynamicLabel)

    def loadingPicture3(self):
        """Loads a image new method."""
        if self.pictureByte:
            self.imageStart = False
            picturePath = Path('.').resolve() / "Images" / self.pictureFile
            self.fileJPG = open(picturePath, "wb")
            self.fileJPG.write(bytes(self.pictureByte))
            self.fileJPG.close()
            pixmap = QPixmap(picturePath)
            self.labelPicture.setPixmap(pixmap)
            self.pictureByte.clear()

    def saveImageEnable(self):
        """Current image can be saved"""
        if self.saveImage:
            self.saveImage = False
        else:
            self.saveImage = True

    def dabGetTime(self):
        """Provides DAB time and date Information (case response 0xBC)."""
        year = self.bufferIn[9] * 256 + self.bufferIn[8]
        months = self.bufferIn[10]
        days = self.bufferIn[11]
        hours = self.bufferIn[12]
        minutes = self.bufferIn[13]
        seconds = self.bufferIn[14]
        date = QDate(year, months, days).toString("d MMMM yyyy")
        time = QTime(hours, minutes, seconds).toString()
        dateTime = "Date: " + date + "  Time: " + time
        self.lineEditDateTime.setText(dateTime)

    def dabGetAudioInfo(self):
        """Provides DAB Audio Information (case response 0xBD)."""
        bitRate = self.bufferIn[9] * 256 + self.bufferIn[8]
        self.labelBitRate.setText("Bit Rate: " + str(bitRate) + " kbps")
        sampleRate = (self.bufferIn[11] * 256 + self.bufferIn[10]) / 1000
        self.labelSampleRate.setText("Sample Rate: " + str(sampleRate) + " kHz")

    def dabGetServiceInfo(self):
        """Provides DAB service information (case response  0xC0)."""
        currentService = chr(self.bufferIn[12]) + chr(self.bufferIn[13]) + chr(self.bufferIn[14]) \
                         + chr(self.bufferIn[15]) + chr(self.bufferIn[16]) + chr(self.bufferIn[17]) \
                         + chr(self.bufferIn[18]) + chr(self.bufferIn[19]) + chr(self.bufferIn[20]) \
                         + chr(self.bufferIn[21]) + chr(self.bufferIn[22]) + chr(self.bufferIn[23]) \
                         + chr(self.bufferIn[24]) + chr(self.bufferIn[25]) + chr(self.bufferIn[26]) \
                         + chr(self.bufferIn[27]) + chr(self.bufferIn[27])
        self.lineEditCurrentService.setText(currentService)

    def tuningForNewEnsemble(self):
        """Tuning For New Ensemble"""
        self.progressBarRSSI.setValue(0)
        self.progressBarSNR.setValue(0)
        self.progressBarCNR.setValue(0)
        self.progressBarFIC.setValue(0)
        self.labelRSSI.setText("00 dB V")
        self.labelSNR.setText("00 DB")
        self.labelCNR.setText("00 dB")
        self.labelFIC.setText("000")
        self.labelBitRate.setText("Bit Rate: ")
        self.labelSampleRate.setText("Sample Rate: ")
        self.ensemble.show()
        self.ensemble.setLabel("Tuning for a new ensemble")
        self.ensemble.setProgressBarValue(0)
        self.timerNewEnsemble.start(300) # Starts updating the ensemble panel with a progress bar
                                         # that advances by 10% after 300 ms
                                         # and closes at the end

    def timerNewEnsembleTick(self):
        """Timer New Ensemble Tick"""
        if self.ensemble.getProgressBarValue() == 100:
            self.timerNewEnsemble.stop()
            self.ensemble.close()
        else:
            newValue = self.ensemble.getProgressBarValue() + 10
            self.ensemble.setProgressBarValue(newValue)


    def loadServices(self):
        """Loads Services"""
        if self.nbServices != 0 :
            for row in range(0, self.nbServices):
                self.tableWidgetViewServices.setItem(row, 0, QTableWidgetItem(self.services[row].preset))
                self.tableWidgetViewServices.setItem(row, 1, QTableWidgetItem(self.services[row].serviceName))
                self.tableWidgetViewServices.setItem(row, 2, QTableWidgetItem(self.services[row].serviceID))
                self.tableWidgetViewServices.setItem(row, 3, QTableWidgetItem(self.services[row].componentID))
                self.tableWidgetViewServices.setItem(row, 4, QTableWidgetItem(self.services[row].tuneIndex))
                self.tableWidgetViewServices.setItem(row, 5, QTableWidgetItem(self.services[row].tuneFrequency))
                self.tableWidgetViewServices.setItem(row, 6, QTableWidgetItem(self.services[row].EID))
                self.tableWidgetViewServices.setItem(row, 7, QTableWidgetItem(self.services[row].componentLabel))
            self.lineEditArtistDLS.setText("Select a Service from the list")
        else :
            msgBox3 = QMessageBox()
            msgBox3.setWindowTitle("DAB WARNING")
            msgBox3.setText("Services list is empty : scan for services")
            msgBox3.setStandardButtons(QMessageBox.StandardButton.Ok)
            if msgBox3.exec() == QMessageBox.StandardButton.Ok:
                pass
            else:
                pass

    def dataGridViewServicesCellClick(self):
        """
        Data Grid View Services Cell Click
        Set Data Services
        return: row
        """
        row = self.tableWidgetViewServices.currentRow()
        self.currentIndex = row
        self.startService()

    def startService(self):
        """Starts the selected service on data grid panel or presets panel"""
        row = self.currentIndex
        self.bufferOut[1] = 0x81
        self.bufferOut[2] = 0x00
        tuneIndex = int(self.services[row].tuneIndex)
        self.bufferOut[3] = tuneIndex
        self.bufferOut[4] = 0x00

        serviceID = int(self.services[row].serviceID, 16)
        self.bufferOut[5] = serviceID & 255
        self.bufferOut[6] = int((serviceID & 65280) / 256)
        self.bufferOut[7] = int((serviceID & 16711680) / 65536)
        self.bufferOut[8] = int((serviceID & 4278190080) / 16777216)

        componentID = int(self.services[row].componentID, 16)
        self.bufferOut[9] = componentID & 255
        self.bufferOut[10] = int((componentID & 65280) / 256)
        self.bufferOut[11] = int((componentID & 16711680) / 65536)
        self.bufferOut[12] = int((componentID & 4278190080) / 16777216)

        self.bufferOut[13] = 0x00
        self.bufferOut[14] = 0x00
        self.bufferOut[15] = 0x00

        self.hidToSend = True
        self.hidSendCheck()

    def buttonScanClick(self):
        """Scans for available DAB+ radio stations.
        """
        self.tableWidgetViewServices.clear()
        headerH = ['Preset','Service Name', 'Service ID', 'Component ID', 'Tune Index', 'Tune Frequency kHz', 'EID',
                   'Component Label']
        self.tableWidgetViewServices.setHorizontalHeaderLabels(headerH)

        self.nbServices = 0
        self.totalServices = 0
        self.progressBarRSSI.setValue(0)
        self.progressBarSNR.setValue(0)
        self.progressBarCNR.setValue(0)
        self.progressBarFIC.setValue(0)
        self.labelRSSI.setText("00 dBµV")
        self.labelSNR.setText("00 dB")
        self.labelCNR.setText("00 dB")
        self.labelFIC.setText("000")
        self.labelBitRate.setText("Bit Rate: ")
        self.labelSampleRate.setText("Sample Rate: ")
        self.bufferOut[0] = 0x00
        self.bufferOut[1] = 0x40
        self.bufferOut[2] = 0x01
        self.bufferOut[3] = 0x00
        self.bufferOut[4] = 0x00
        self.bufferOut[5] = 0x00
        self.bufferOut[6] = 0x00
        self.bufferOut[7] = 0x00
        self.bufferOut[8] = 0x00
        self.bufferOut[9] = 0x00
        self.bufferOut[10] = 0x00
        self.bufferOut[11] = 0x00
        self.bufferOut[12] = 0x00
        self.bufferOut[13] = 0x00
        self.bufferOut[14] = 0x00
        self.bufferOut[15] = 0x00
        self.service.show()
        self.service.labelScanning.setText("running ...")
        self.service.tableWidgetService.clearContents()
        self.service.pushButtonClose.setEnabled(False)
        self.hidToSend = True
        self.hidSendCheck()

# PRESETS DAB+ RADIO
    def presetsButtonDisabled(self):
        """All presets buttons are disabled"""
        self.pushButtonPreset1.setEnabled(False)
        self.pushButtonPreset2.setEnabled(False)
        self.pushButtonPreset3.setEnabled(False)
        self.pushButtonPreset4.setEnabled(False)
        self.pushButtonPreset5.setEnabled(False)
        self.pushButtonPreset6.setEnabled(False)
        self.pushButtonPreset7.setEnabled(False)
        self.pushButtonPreset8.setEnabled(False)
        self.pushButtonPreset9.setEnabled(False)
        self.pushButtonPreset10.setEnabled(False)
        self.pushButtonPreset11.setEnabled(False)
        self.pushButtonPreset12.setEnabled(False)

    def presetsButtonEnabled(self):
        """All presets buttons are enabled"""
        self.pushButtonPreset1.setEnabled(True)
        self.pushButtonPreset2.setEnabled(True)
        self.pushButtonPreset3.setEnabled(True)
        self.pushButtonPreset4.setEnabled(True)
        self.pushButtonPreset5.setEnabled(True)
        self.pushButtonPreset6.setEnabled(True)
        self.pushButtonPreset7.setEnabled(True)
        self.pushButtonPreset8.setEnabled(True)
        self.pushButtonPreset9.setEnabled(True)
        self.pushButtonPreset10.setEnabled(True)
        self.pushButtonPreset11.setEnabled(True)
        self.pushButtonPreset12.setEnabled(True)

    def buttonMemoryClick(self):
        """ If pushButton is clicked, a new Presets list must be modified"""
        if self.memory == False:
            self.memory = True
            self.resetPresets()
        else:
            self.memory = False

    def resetPresets(self):
        """Resets all presets and allows you to modify the list of presets"""
        msgBox6 = QMessageBox()
        msgBox6.setWindowTitle("DAB WARNING")
        msgBox6.setText('You can modify the list and order of the presets in the "Services List" table (under the "Presets" column): 0 indicates the selected preset, while 1, 2, 3, etc., determine the preset order. To apply the changes, click "Save this services list," then click "Off" followed by "On" to refresh the presets.')
        msgBox6.setInformativeText("Are you sure?")
        msgBox6.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        answer = msgBox6.exec()
        if answer == QMessageBox.StandardButton.Yes:
            # self.buttonPresetNoClicked()
            self.presetsButtonDisabled()
            self.pushButtonMemory.setEnabled(False)
        if answer == QMessageBox.StandardButton.No:
            pass

    def loadPresets(self):
        """Loads all presets"""
        self.pushButtonMemory.setEnabled(True)
        for index in range(self.nbPresets):
            match index:
                case 0:
                    self.pushButtonPreset1.setText(self.presets[0].serviceName.strip())
                    self.pushButtonPreset1.setEnabled(True)
                case 1:
                    self.pushButtonPreset2.setText(self.presets[1].serviceName.strip())
                    self.pushButtonPreset2.setEnabled(True)
                case 2:
                    self.pushButtonPreset3.setText(self.presets[2].serviceName.strip())
                    self.pushButtonPreset3.setEnabled(True)
                case 3:
                    self.pushButtonPreset4.setText(self.presets[3].serviceName.strip())
                    self.pushButtonPreset4.setEnabled(True)
                case 4:
                    self.pushButtonPreset5.setText(self.presets[4].serviceName.strip())
                    self.pushButtonPreset5.setEnabled(True)
                case 5:
                    self.pushButtonPreset6.setText(self.presets[5].serviceName.strip())
                    self.pushButtonPreset6.setEnabled(True)
                case 6:
                    self.pushButtonPreset7.setText(self.presets[6].serviceName.strip())
                    self.pushButtonPreset7.setEnabled(True)
                case 7:
                    self.pushButtonPreset8.setText(self.presets[7].serviceName.strip())
                    self.pushButtonPreset8.setEnabled(True)
                case 8:
                    self.pushButtonPreset9.setText(self.presets[8].serviceName.strip())
                    self.pushButtonPreset9.setEnabled(True)
                case 9:
                    self.pushButtonPreset10.setText(self.presets[9].serviceName.strip())
                    self.pushButtonPreset10.setEnabled(True)
                case 10:
                    self.pushButtonPreset11.setText(self.presets[10].serviceName.strip())
                    self.pushButtonPreset11.setEnabled(True)
                case 11:
                    self.pushButtonPreset12.setText(self.presets[11].serviceName.strip())
                    self.pushButtonPreset12.setEnabled(True)
                case _:
                    pass

    def savePresetsMark(self):
        """Saves Presets marks into json Services File"""
        # Creating the json object
        settings = {}
        for row in range(0, self.nbServices):
            preset = self.services[row].preset
            serviceName = self.services[row].serviceName
            serviceId = self.services[row].serviceID
            componentID = self.services[row].componentID
            tuneIndex = self.services[row].tuneIndex
            tuneFrequency = self.services[row].tuneFrequency
            EID = self.services[row].EID
            componentLabel = self.services[row].componentLabel
            serviceIndex = "service" + str(row + 1)
            serviceDict = {
                "preset": preset,
                "serviceName": serviceName,
                "serviceID": serviceId,
                "componentID": componentID,
                "tuneIndex": tuneIndex,
                "tuneFrequency": tuneFrequency,
                "EID": EID,
                "componentLabel": componentLabel
            }
            settings[serviceIndex] = serviceDict
        # Serializing Json
        json_object = json.dumps(settings, indent=7)

        # Updating or creating the json file
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Services json File", "", "Json Files (*.json)")
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    file.write(json_object)  # json file
            except Exception as e:
                pass

    def buttonPresetNoClicked(self):
    #     """Makes all the buttons Enable style"""
        styleButton = 'QPushButton {background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(84, 84, 84, 255),stop:1 rgba(59, 59, 59, 255)); \
        min-width: 30px; border-style: solid; border-width: 1px; border-radius: 3px; border-color: #051a39; padding: 3px;}'

        self.pushButtonPreset1.setStyleSheet(styleButton)
        self.pushButtonPreset2.setStyleSheet(styleButton)
        self.pushButtonPreset3.setStyleSheet(styleButton)
        self.pushButtonPreset4.setStyleSheet(styleButton)
        self.pushButtonPreset5.setStyleSheet(styleButton)
        self.pushButtonPreset6.setStyleSheet(styleButton)
        self.pushButtonPreset7.setStyleSheet(styleButton)
        self.pushButtonPreset8.setStyleSheet(styleButton)
        self.pushButtonPreset9.setStyleSheet(styleButton)
        self.pushButtonPreset10.setStyleSheet(styleButton)
        self.pushButtonPreset11.setStyleSheet(styleButton)
        self.pushButtonPreset12.setStyleSheet(styleButton)

    def buttonPresetClick(self, index):
        """Selects a favorite (preset).
        :param index: index of the chosen favorite.
        """
        self.buttonPresetNoClicked()
        match index:
            case 0:
                self.pushButtonPreset1.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = self.presets[index].serviceID
                print(serviceID)
                self.favorite(serviceID)
            case 1:
                self.pushButtonPreset2.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = self.presets[index].serviceID
                self.favorite(serviceID)
            case 2:
                self.pushButtonPreset3.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = self.presets[index].serviceID
                self.favorite(serviceID)
            case 3:
                self.pushButtonPreset4.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = self.presets[index].serviceID
                self.favorite(serviceID)
            case 4:
                self.pushButtonPreset5.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = self.presets[index].serviceID
                self.favorite(serviceID)
            case 5:
                self.pushButtonPreset6.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = self.presets[index].serviceID
                self.favorite(serviceID)
            case 6:
                self.pushButtonPreset7.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = self.presets[index].serviceID
                self.favorite(serviceID)
            case 7:
                self.pushButtonPreset8.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = self.presets[index].serviceID
                self.favorite(serviceID)
            case 8:
                self.pushButtonPreset9.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = self.presets[index].serviceID
                self.favorite(serviceID)
            case 9:
                self.pushButtonPreset10.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = self.presets[index].serviceID
                self.favorite(serviceID)
            case 10:
                self.pushButtonPreset11.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = self.presets[index].serviceID
                self.favorite(serviceID)
            case 11:
                self.pushButtonPreset12.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = self.presets[index].serviceID
                self.favorite(serviceID)

    def favorite(self, serviceID):
        """Searches this preset in the services list and start this service."""
        self.nbServices = len(self.services)
        self.currentIndex = 0
        if self.nbServices != 0 :
            for row in range(0, self.nbServices):
                if self.services[row].serviceID == serviceID :
                    self.currentIndex = row
            self.startService()

    def checkBoxArtistTitleClick(self):
        """The artist's name is displayed separately or not."""
        if self.checkBoxArtistTitle.isChecked():
            self.softLabelsArtistTitle()
        else:
            self.lineEditTitle.setText("")
            self.lineEditArtistDLS.setText(self.dynamicLabel)

    def checkBoxMuteClick(self):
        """Selects whether to use silent mode."""
        self.bufferOut[0] = 0x00
        self.bufferOut[1] = 0x13
        self.bufferOut[2] = 0x00
        self.bufferOut[3] = 0x01
        self.bufferOut[4] = 0x03
        if self.checkBoxMute.isChecked():
            self.bufferOut[5] = 0x03
        else:
            self.bufferOut[5] = 0x00
        self.bufferOut[6] = 0x00
        self.bufferOut[7] = 0x00
        self.bufferOut[8] = 0x00
        self.bufferOut[9] = 0x00
        self.bufferOut[10] = 0x00
        self.bufferOut[11] = 0x00
        self.bufferOut[12] = 0x00
        self.bufferOut[13] = 0x00
        self.bufferOut[14] = 0x00
        self.bufferOut[15] = 0x00
        self.hidToSend = True
        self.hidSendCheck()

    def checkBoxMonoClick(self):
        """Selects Mono or Stereo mode."""
        self.bufferOut[0] = 0x00
        self.bufferOut[1] = 0x13
        self.bufferOut[2] = 0x00
        self.bufferOut[3] = 0x02  # Property 0x0302. AUDIO_OUTPUT_CONFIG
        self.bufferOut[4] = 0x03
        if self.checkBoxMono.isChecked():
            self.bufferOut[5] = 0x01
        else:
            self.bufferOut[5] = 0x00
        self.bufferOut[6] = 0x00
        self.bufferOut[7] = 0x00
        self.bufferOut[8] = 0x00
        self.bufferOut[9] = 0x00
        self.bufferOut[10] = 0x00
        self.bufferOut[11] = 0x00
        self.bufferOut[12] = 0x00
        self.bufferOut[13] = 0x00
        self.bufferOut[14] = 0x00
        self.bufferOut[15] = 0x00
        self.hidToSend = True
        self.hidSendCheck()

    def hScrollBarVolumeValueChanged(self):
        """
        When the volume's scrollbar changes, the volume is modified.
        """
        self.volume()

    def volume(self):
        """
        Changes the volume.
        """
        # self.labelVolume = str(self.horizontalScrollBarVolume.value())
        self.bufferOut[0] = 0x00
        self.bufferOut[1] = 0x13
        self.bufferOut[2] = 0x00
        self.bufferOut[3] = 0x00
        self.bufferOut[4] = 0x03  # Property 0x0300. AUDIO_ANALOG_VOLUME
        self.bufferOut[5] = self.horizontalScrollBarVolume.value()
        self.bufferOut[6] = 0x00
        self.bufferOut[7] = 0x00
        self.bufferOut[8] = 0x00
        self.bufferOut[9] = 0x00
        self.bufferOut[10] = 0x00
        self.bufferOut[11] = 0x00
        self.bufferOut[12] = 0x00
        self.bufferOut[13] = 0x00
        self.bufferOut[14] = 0x00
        self.bufferOut[15] = 0x00
        self.hidToSend = True
        self.hidSendCheck()

    def hidSendCheck(self):
        """
        Timer HID Send Tick
        """
        if self.hidToSend:  # True
            self.hidSend()
            if self.bufferOut[1] == 0x81:
                # Image clear
                self.lineEditArtistDLS.setText("")
                self.lineEditTitle.setText("")
                self.lineEditPictureName.setText("")
                self.lineEditPacket.setText("")
                self.lineEditCurrentService.setText("")
                self.lineEditDateTime.setText("")
                self.labelBitRate.setText("Bit Rate : ")
                self.labelSampleRate.setText("Sample Rate : ")
                self.imageStart = False
                self.pictureByte.clear()
        else:
            self.hidToSend = False

    def hidSend(self):
    # def hidSend(self, dataOut=b"\x00"):
        """Sends a command for the USB HID device
        HID Send
        dataOut: byte, command to the device
        """
        Out = ' '.join('{:02X}'.format(a) for a in self.bufferOut)
        self.lineEditBufferOut.setText(Out)
        # dataOut=b"\x00 ...
        dataOut = bytes(bytearray(self.bufferOut))

        try:
            res1 = self.myDevice.write(dataOut)
            dataOutStr = ""
            for data in dataOut:
                dataOutStr += str("{0:02X}".format(data)) + " "
        except UsbHidIOError:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Message")
            msgBox.setText("Writing error")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Cancel)
            msgBox.setDefaultButton(QMessageBox.StandardButton.Cancel)
            answer = msgBox.exec()
            if answer == QMessageBox.StandardButton.Cancel:
                pass

def loadStyleSheet(app, qssFile):
    """Loads the qss file that defines the application style."""
    file = QFile(qssFile)
    if file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        styleSheet = file.readAll().data().decode("utf-8")
        app.setStyleSheet(styleSheet)


def main():
    """Main program"""
    app = QApplication(sys.argv)

    # Load the Combinear.qss style sheet
    loadStyleSheet(app, "qss/Combinear.qss")

    window = Dab()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
