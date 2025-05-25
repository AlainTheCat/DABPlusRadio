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
import hid
import json
from MainWindow import Ui_Form
from PySide6.QtWidgets import QMainWindow, QMessageBox, QApplication, QTableWidgetItem, QFileDialog
from PySide6.QtCore import QTimer, QObject, Signal, QDate, QTime, QByteArray, QFile
from PySide6.QtGui import QIcon, QPixmap, QImage
from qled import QLed
from serviceTable import TableService
from ensemblePanel import Ensemble

class Communicate(QObject):
    updateDisplay = Signal(int)

class Preset:
    """
         Available services
        ...
    Attributes:


    """

    def __init__(self, serviceName, serviceID, componentID, tuneIndex, tuneFrequency, EID, componentLabel, enable):
        """ initializes Service class """
        self.serviceName = serviceName
        self.serviceID = serviceID
        self.componentID = componentID
        self.tuneIndex = tuneIndex
        self.tuneFrequency = tuneFrequency
        self.EID = EID
        self.componentLabel = componentLabel
        self.enable = enable

class Service:
    """
         Available services
        ...
    Attributes:


    """

    def __init__(self, serviceName, serviceID, componentID, tuneIndex, tuneFrequency, EID, componentLabel):
        """ initializes Service class """
        self.serviceName = serviceName
        self.serviceID = serviceID
        self.componentID = componentID
        self.tuneIndex = tuneIndex
        self.tuneFrequency = tuneFrequency
        self.EID = EID
        self.componentLabel = componentLabel


# Creating list of services
services = []

# List all services (services1.json)
with open("service.json") as f:
    data1 = json.load(f)

nbServices = sum([1 for i in data1])

print("Number of Services: ", nbServices)

# Appending instances to list
for i in range(1, nbServices + 1):
    services.append(
        Service(
            data1["service" + str(i)]["serviceName"],
            data1["service" + str(i)]["serviceID"],
            data1["service" + str(i)]["componentID"],
            data1["service" + str(i)]["tuneIndex"],
            data1["service" + str(i)]["tuneFrequency"],
            data1["service" + str(i)]["EID"],
            data1["service" + str(i)]["componentLabel"]
        )
    )

#  Creating list of presets
presets = []

# loading these presets from presets.json
with open("presets.json") as f:
    data2 = json.load(f)

# Appending instances to list
for i in range(12):
    presets.append(
        Preset(
            data2["preset" + str(i)]["serviceName"],
            data2["preset" + str(i)]["serviceID"],
            data2["preset" + str(i)]["componentID"],
            data2["preset" + str(i)]["tuneIndex"],
            data2["preset" + str(i)]["tuneFrequency"],
            data2["preset" + str(i)]["EID"],
            data2["preset" + str(i)]["componentLabel"],
            data2["preset" + str(i)]["enable"]
        )
    )

DLS_Ascii = [32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32,
             32, 32, 32, 32, 32, 32, 32, 32, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
             48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,
             72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95,
             96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115,
             116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 32, 225, 224, 233, 232, 237, 236, 243,
             242, 250, 249, 209, 199, 32, 223, 161, 32, 226, 228, 234, 235, 238, 239, 244, 246, 251, 252, 241,
             231, 32, 32, 32, 32, 170, 32, 169, 137, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 186, 185,
             178, 179, 177, 32, 32, 32, 181, 191, 247, 176, 188, 189, 190, 167, 193, 192, 201, 200, 205, 204,
             211, 210, 218, 217, 32, 32, 154, 142, 208, 32, 194, 196, 202, 203, 206, 207, 212, 214, 219, 220,
             32, 32, 32, 158, 32, 32, 32, 197, 198, 140, 32, 253, 213, 216, 254, 32, 32, 32, 32, 32, 32, 32,
             227, 229, 230, 156, 32, 253, 245, 248, 32, 32, 32, 32, 32, 32, 32, 32]

def savePresets():
    """
    Save all presets on json file "presets.json"
    """
    settings = {}
    it = 0
    for preset in presets:
        serviceName = preset.serviceName
        serviceId = preset.serviceID
        componentID = preset.componentID
        tuneIndex = preset.tuneIndex
        tuneFrequency = preset.tuneFrequency
        EID = preset.EID
        componentLabel = preset.componentLabel
        enable = preset.enable
        presetIndex = "preset" + str(it)
        presetDict = {
            "serviceName": serviceName,
            "serviceID": serviceId,
            "componentID": componentID,
            "tuneIndex": tuneIndex,
            "tuneFrequency": tuneFrequency,
            "EID": EID,
            "componentLabel": componentLabel,
            "enable": enable
        }
        settings[presetIndex] = presetDict
        it += 1
    # Serializing Json
    json_object = json.dumps(settings, indent = 7)
    with open("presets.json", "w") as outfile:
        outfile.write(json_object)


def checkDevice():
    """
    Check the device.
    """
    VENDOR_ID = 0x1234
    PRODUCT_ID = 0x4684
    try:
        device = hid.Device(vid=VENDOR_ID, pid=PRODUCT_ID)
        return device
    except Exception:
        try:
            res = hid.enumerate(vid=VENDOR_ID, pid=PRODUCT_ID)
            dict1 = res[0]
            hidPath = dict1["path"].decode()
            print("sudo chmod 0666 " + hidPath)
            msgBox1 = QMessageBox()
            msgBox1.setWindowTitle("DEVICE ERROR")
            msgBox1.setText("Device can't open")
            msgBox1.setInformativeText("sudo chmod 0666 " + hidPath)
            msgBox1.setStandardButtons(QMessageBox.StandardButton.Ok)
            if msgBox1.exec() == QMessageBox.StandardButton.Ok:
                exit()
            else:
                pass

        except Exception:
            msgBox2 = QMessageBox()
            msgBox2.setWindowTitle("DEVICE ERROR")
            msgBox2.setText("Device no found")
            msgBox2.setInformativeText("Plug your device !")
            msgBox2.setStandardButtons(QMessageBox.StandardButton.Ok)
            if msgBox2.exec() == QMessageBox.StandardButton.Ok:
                exit()
            else:
                pass


class Dab(QMainWindow, Ui_Form):
    """
    DAB Radio panel (creating and playing)
    """

    def __init__(self):
        """Initializes the MainWindow class"""
        super().__init__()

        # ---INIT PANEL ---

        self.setupUi(self)
        self.setWindowIcon(QIcon("radio.png"))
        self.setWindowTitle("RADIO DAB")

        # --- INIT SOME VARIABLE ---
        # Read and write buffers
        # IN -> Read from the Device
        # Received data will be stored here - the first byte in the array is unused
        # bufferInSize = 40  -> Size of the data buffer coming IN to the PC
        self.bufferIn = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        # OUT -> Write to the device
        # Transmitted data is stored here - the first item in the array must be 0
        # bufferOutSize = 16  -> Size of the data buffer going OUT from the PC
        self.bufferOut = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                          0x00]

        self.hidToSend = False

        self.currentIndex = 0
        self.totalServices = 0

        self.dynamicLabel = "Alain is - the best"
        self.artist = ""
        self.title = ""
        self.packetIndex = 0
        self.PADDataType = 0
        self.DLSType = 0
        self.MOTDLSType = 0
        self.DLSLength = 0
        self.SLSLength = 0
        self.payloadLength = 0

        self.jackStatus = 0x00  # Analog or Optical output
        self.labelVolume = "0"

        self.imageStart = False  # Beginning for load the picture
        self.pathPicture = ""  # Path of the picture
        self.pictureHex = ""  # Content of the picture in hexa
        self.pictureByte = QByteArray()  # Content of the picture in Byte format
        self.pictureFile = "picture.jpg"  # Picture name for init
        self.pictureResult = []  # Content array  of the picture
        self.fileJPG = QFile # File for load Image

        # --- INIT DEVICE ---

        self.myDevice = checkDevice()
        # print(self.myDevice)

        # --- INIT SOME WIDGET ---

        self.pushButtonOn.setEnabled(True)
        self.pushButtonOff.setEnabled(False)
        self.pushButtonScan.setEnabled(False)
        self.checkBoxMute.setEnabled(False)
        self.checkBoxMono.setEnabled(False)
        self.checkBoxArtistTitle.setEnabled(False)
        self.tableWidgetViewServices.setEnabled(False)
        self.horizontalScrollBarVolume.setEnabled(False)
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
        self.my_array = [[0 for col in range(5)] for row in range(40)]

        headerH = ['Service Name', 'Service ID', 'Component ID', 'Tune Index', 'Tune Frequency kHz', 'EID',
                   'Component Label']
        self.tableWidgetViewServices.setHorizontalHeaderLabels(headerH)

        # --- INIT CONNECTIONS ---
        self.pushButtonOn.clicked.connect(self.on)
        self.pushButtonOff.clicked.connect(self.off)
        self.pushButtonScan.clicked.connect(self.buttonScanClick)

        self.horizontalScrollBarVolume.valueChanged.connect(self.hScrollBarVolumeValueChanged)

        self.tableWidgetViewServices.clicked.connect(self.dataGridViewServicesCellClick)

        self.checkBoxMono.clicked.connect(self.checkBoxMonoClick)
        self.checkBoxMute.clicked.connect(self.checkBoxMuteClick)

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
        self.pushButtonTest1.clicked.connect(self.test1)
        self.pushButtonTest2.clicked.connect(self.test2)
        self.pushButtonTest3.clicked.connect(self.test3)
        # self.pushButtonTest4.clicked.connect(self.timer4Tick)
        self.pushButtonTest5.clicked.connect(self.test5)
        self.pushButtonTest6.clicked.connect(self.loadServices)
        self.pushButtonTest7.clicked.connect(self.test7)
        self.pushButtonTest8.clicked.connect(self.test8)
        self.pushButtonTest9.clicked.connect(self.test9)
        self.pushButtonTest10.clicked.connect(self.test10)

        self.com = Communicate()

        # --- INIT TIMERS ---
        # Power Up -> delay 100 mSec
        self.timerPowerUp = QTimer()
        self.timerPowerUp.timeout.connect(self.open)

        # Power Down -> delay one shot 50 mSec
        self.timerPowerDown = QTimer()
        self.timerPowerDown.timeout.connect(self.close)

        # Artist Title -> delay one shot 100 mSec
        self.timerArtistTitle = QTimer()
        # self.timerArtistTitle.connect(self.timerArtistTitleTick)

        # New Ensemble -> delay one shot 300 mSec
        self.timerNewEnsemble = QTimer()
        self.timerNewEnsemble.timeout.connect(self.timerNewEnsembleTick())

        # Read device -> periodic delay 50 mSec
        self.timerReadDevice = QTimer()
        self.timerReadDevice.timeout.connect(self.readDevice)

        # HID to send -> delay 50 mSec
        # self.timerHidToSend = QTimer()
        # self.timerHidToSend.timeout.connect(self.timerHidToSendTick())


    def off(self):
        """
        Power Off
        """
        self.toolStripStatusLabel1.setText("DAB Tuner Disconnected")
        self.toolStripStatusLabel2.setText("")
        self.toolStripStatusLabel3.setText("")
        self.toolStripStatusLabel4.setText("")
        self.pushButtonOn.setEnabled(True)
        self.pushButtonOff.setEnabled(False)
        self.presetsButtonDisabled()
        self.clearPanel()
        self.clearTextBox()
        self.timerPowerDown.start(50)

    def close(self):
        """
        Stand by the device.
        """
        self.timerPowerDown.stop()
        self.horizontalScrollBarVolume.setValue(0)
        self.bufferOut[0] = 0x00
        self.bufferOut[1] = 0x00  # Stand by the device ( stop the HID coming IN to the PC )
        self.led.toggleValue()
        # self.hidToSend = True
        self.hidSend()
        """
        dataOut = ' '.join('{:02X}'.format(a) for a in self.bufferOut)
        self.lineEditBufferOut.setText(dataOut)
        order = bytes(bytearray(self.bufferOut))
        self.hidSend(order)
        """


    def clearPanel(self):
        """
        Clear this panel.
        """
        self.labelRSSI.setText("0 db V")
        self.labelSNR.setText("0 dB")
        self.labelCNR.setText("0 dB")
        self.labelFIC.setText("0")
        self.checkBoxMono.setEnabled(False)
        self.checkBoxMute.setEnabled(False)
        self.horizontalScrollBarVolume.setEnabled(False)

    def clearTextBox(self):
        """
        Clear all TextBox (lineEdit)
        """
        self.lineEditCurrentService.setText("")
        self.lineEditArtistDLS.setText("")
        self.lineEditTitle.setText("")
        # self.lineEditBufferIn.setText("")
        # self.lineEditBufferOut.setText("")
        self.lineEditPacket.setText("")
        self.lineEditPictureName.setText("")
        self.lineEditDateTime.setText("")

    def on(self):
        """
        Power On
        """
        self.loadPresets()
        self.loadServices()

        self.toolStripStatusLabel1.setText("DAB Tuner connected")
        self.toolStripStatusLabel2.setText("")
        self.toolStripStatusLabel3.setText("")
        self.toolStripStatusLabel4.setText("")
        self.pushButtonOn.setEnabled(False)
        self.pushButtonOff.setEnabled(True)
        self.horizontalScrollBarVolume.setEnabled(True)
        self.checkBoxMono.setEnabled(True)
        self.checkBoxMute.setEnabled(True)
        self.checkBoxArtistTitle.setEnabled(True)
        self.pushButtonScan.setEnabled(True)

        self.timerPowerUp.start(100)

    def open(self):
        """a HID device has been plugged in..."""
        self.timerPowerUp.stop()
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
        self.led.toggleValue()
        # self.hidToSend = True
        self.hidSend()
        """
        dataOut = ' '.join('{:02X}'.format(a) for a in self.bufferOut)
        self.lineEditBufferOut.setText(dataOut)
        order = bytes(bytearray(self.bufferOut))
        self.hidSend(order)
        """
        self.timerReadDevice.start(50)

    def readDevice(self):
        """Reads the device"""
        # print("Device reading ...")
        # self.timer.stop()
        try:
            self.bufferIn = self.myDevice.read(size=40, timeout=1)
            if self.bufferIn:
                dataInHex = ' '.join('{:02X}'.format(a) for a in self.bufferIn)
                self.lineEditBufferIn.setText(dataInHex)
                print(dataInHex)
                # print('{:02X}'.format(self.dataAddress))
                self.onRead()
        except Exception:
            pass
            """
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Message")
            msgBox.setText("Reading error")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Cancel)
            msgBox.setDefaultButton(QMessageBox.StandardButton.Cancel)
            answer = msgBox.exec()
            if answer == QMessageBox.StandardButton.Cancel:
                pass
            """

    def onRead(self):
        """
        Read bytes in bufferIn from the microcontroller...
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
                self.serviceListNotAvailable()

    def partInfo(self):
        """
        Part Info
        """
        # print("Part Info")
        Skyworks_Part_Number = str(self.bufferIn[13] * 256 + self.bufferIn[12])
        Microchip_Part_Number = chr(self.bufferIn[27]) + chr(self.bufferIn[28]) + chr(self.bufferIn[29]) + \
                                chr(self.bufferIn[30]) + chr(self.bufferIn[31]) + chr(self.bufferIn[32]) + \
                                chr(self.bufferIn[33]) + chr(self.bufferIn[34]) + chr(self.bufferIn[35]) + \
                                chr(self.bufferIn[36]) + chr(self.bufferIn[37]) + chr(self.bufferIn[38])
        partInfoText = Microchip_Part_Number + " / Si" + Skyworks_Part_Number
        self.toolStripStatusLabel2.setText(partInfoText)

    def systemState(self):
        """
        System State
        """
        # print("System State")

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
        # print(Image_System)
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
                # self.hidSend()
                """
                dataOut = ' '.join('{:02X}'.format(a) for a in self.bufferOut)
                self.lineEditBufferOut.setText(dataOut)
                order = bytes(bytearray(self.bufferOut))
                self.hidSend(order)
                """
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
        """
        Give SI firmware and PIC firmware
        """
        # print("firmware")

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
        """
        Digital Service List

        """
        countServices = 0
        totalServices = 0
        # print("Digital Service List")
        serviceID = str(self.bufferIn[15]) + " " + str(self.bufferIn[14]) + \
                    " " + str(self.bufferIn[13]) + " " + str(self.bufferIn[12])
        print(serviceID)
        serviceName = str(self.bufferIn[20]) + str(self.bufferIn[21]) + str(self.bufferIn[22]) \
                      + str(self.bufferIn[23]) + str(self.bufferIn[25]) + str(self.bufferIn[26]) \
                      + str(self.bufferIn[27]) + str(self.bufferIn[28]) + str(self.bufferIn[29]) \
                      + str(self.bufferIn[30]) + str(self.bufferIn[31]) + str(self.bufferIn[32]) \
                      + str(self.bufferIn[33]) + str(self.bufferIn[34]) + str(self.bufferIn[35])
        print(serviceName)
        componentID = str(self.bufferIn[39]) + " " + str(self.bufferIn[38]) + \
                    " " + str(self.bufferIn[37]) + " " + str(self.bufferIn[36])
        print(componentID)
        if self.bufferOut[1] == 0x40:
            countServices += 1
            totalServices += 1
        # print(countServices)
        # print(totalServices)
        rowPosition = self.tableWidgetViewServices.rowCount()
        self.tableWidgetViewServices.insertRow(rowPosition)
        self.tableWidgetViewServices.setItem(rowPosition, 0, QTableWidgetItem(serviceName))
        self.tableWidgetViewServices.setItem(rowPosition, 1, QTableWidgetItem(serviceID))
        self.tableWidgetViewServices.setItem(rowPosition, 2, QTableWidgetItem(componentID))


    def dabDigradStatus(self):
        """
        DAB Digrad Status

        """
        # print("DAB Digrad Status")
        # Tune frequency and index
        tuneFrequency = (self.bufferIn[19] * 0x1000000) + (self.bufferIn[18] * 0x10000) + (self.bufferIn[17] * 0x100) + self.bufferIn[16]
        # print(tuneFrequency)
        tuneIndex = self.bufferIn[20]
        # print(tuneIndex)
        self.my_array[tuneIndex][0] = tuneIndex
        self.my_array[tuneIndex][1] = tuneFrequency
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
        self.my_array[tuneIndex][2] = RSSI
        valid = self.bufferIn[9] & 0x01
        self.my_array[tuneIndex][3] = valid
        SNR = self.bufferIn[11]
        CNR = self.bufferIn[13]
        FICQuality = self.bufferIn[12]
        # nbServices = 0
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
        # print(self.my_array)
        self.service.setArray(self.my_array)

        if self.bufferOut[1] == 0x40:
            # print("scanning " + str(tuneFrequency) + " Mhz")
            self.service.progressBar.setValue(tuneIndex)
            self.service.labelScanning.setText("Scanning: " + str(tuneFrequency) + " Mhz")
            if tuneIndex == 39:
                self.service.labelScanning.setText("Scanning complete")
                self.service.pushButtonClose.setEnabled(True)
                if self.totalServices != 0:
                    self.lineEditArtistDLS = "Select a Service from the list"


    def ensembleInfo(self):
        """
        Ensemble Information
        """
        # print("Ensemble Information")

        EID = str(self.bufferOut[8]) + str(self.bufferIn[9])
        # print(EID)
        componentLabel = chr(self.bufferIn[10]) + chr(self.bufferIn[11]) + chr(self.bufferIn[12]) \
                         + chr(self.bufferIn[13]) + chr(self.bufferIn[14]) + chr(self.bufferIn[15]) \
                         + chr(self.bufferIn[16]) + chr(self.bufferIn[17]) + chr(self.bufferIn[18]) \
                         + chr(self.bufferIn[19]) + chr(self.bufferIn[12]) + chr(self.bufferIn[21]) \
                         + chr(self.bufferIn[22]) + chr(self.bufferIn[23]) + chr(self.bufferIn[24]) \
                         + chr(self.bufferIn[125])
        # print(componentLabel)

    def getDigitalServiceData(self):
        """
        Get Digital Service Data

        """
        # print("Get Digital Service Data")
        pictureName = ""
        self.packetIndex = self.bufferIn[6]
        # print("packetIndex: ", '{:02X}'.format(self.packetIndex))
        if self.packetIndex == 0x00:
            self.PADDataType = self.bufferIn[11]
            print("PADDataType: ", '{:02X}'.format(self.PADDataType))
            match self.PADDataType:
                case 0x80:  # DLS
                    self.DLSType = self.bufferIn[28]
                    print("DLSType: ", '{:02X}'.format(self.DLSType))
                    self.DLSLength = self.bufferIn[22] - 3
                    print("DLSLength: ", '{:02X}'.format(self.DLSLength))
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
                                print("New DLSLength 0: ", '{:02X}'.format(self.DLSLength))
                            else:
                                for var in range(30, self.DLSLength + 30):
                                    # Char  , , , , ,...OK ( &H7F to &HFF )
                                    self.dynamicLabel = self.dynamicLabel + chr(DLS_Ascii[self.bufferIn[var]])
                            print("Dynamic Label: ", self.dynamicLabel)
                            print("New DLSLength 1: ", '{:02X}'.format(self.DLSLength))
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
                            print("New DLSLength 2: ", '{:02X}'.format(self.DLSLength))
                            # self.timerArtistTitle.setInterval(100)
                            self.timerArtistTitle.start()
                        case 0x12:
                            # print("Case: ", 0x12)
                            if self.bufferIn[33] != 0x0 and self.bufferIn[35] != 0x0 and self.bufferIn[36] != 0x0:
                                # print("OK", '{:02X}'.format(self.bufferIn[33]), " ", '{:02X}'.format(self.bufferIn[35]), " ", '{:02X}'.format(self.bufferIn[36]))
                                titleLen = self.bufferIn[33] + 1
                                artistLen = self.bufferIn[36] + 1
                                artistIndex = self.bufferIn[35]
                                self.title = self.dynamicLabel[0: titleLen]
                                # print("Dynamic Label 2: ", self.dynamicLabel)
                                # print("Title: ", self.title)
                                self.artist = self.dynamicLabel[artistIndex: (artistIndex + artistLen)]
                                # print("Artist: ", self.artist)
                                self.lineEditTitle.setText("Title: " + self.title)
                                self.lineEditArtistDLS.setText("Artist: " + self.artist)
                            else:
                                # print("KO", '{:02X}'.format(self.bufferIn[33]), " ", '{:02X}'.format(self.bufferIn[35])," ", '{:02X}'.format(self.bufferIn[36]))
                                if self.checkBoxArtistTitle.isChecked():
                                    self.softLabelsArtistTitle()
                                else:
                                    self.lineEditArtistDLS.setText(self.dynamicLabel)
                        case 0x92:
                            print("Case: ", 0x12)
                            if self.bufferIn[33] != 0x0 and self.bufferIn[35] != 0x0 and self.bufferIn[36] != 0x0:
                                print("OK", '{:02X}'.format(self.bufferIn[33]), " ", '{:02X}'.format(self.bufferIn[35]),
                                      " ", '{:02X}'.format(self.bufferIn[36]))
                                titleLen = self.bufferIn[33] + 1
                                artistLen = self.bufferIn[36] + 1
                                artistIndex = self.bufferIn[35]
                                self.title = self.dynamicLabel[0: titleLen]
                                print("Title: ", self.title)
                                self.artist = self.dynamicLabel[artistIndex: (artistIndex + artistLen)]
                                print("Artist: ", self.artist)
                                self.lineEditTitle.setText("Title: " + self.title)
                                self.lineEditArtistDLS.setText("Artist: " + self.artist)
                            else:
                                print("KO", '{:02X}'.format(self.bufferIn[33]), " ", '{:02X}'.format(self.bufferIn[35]),
                                      " ", '{:02X}'.format(self.bufferIn[36]))
                                if self.checkBoxArtistTitle.isChecked():
                                    self.softLabelsArtistTitle()
                                else:
                                    self.lineEditArtistDLS.setText(self.dynamicLabel)

                case 0x7C:
                    self.MOTSLSType = self.bufferIn[28]  # MOT SLS
                    print("MOTSLSType1: ", '{:02X}'.format(self.MOTSLSType))
                    self.SLSLength = self.bufferIn[35] * 256 + self.bufferIn[36]
                    print("SLSLength: ", '{:02X}'.format(self.SLSLength))
                    match self.MOTSLSType:
                        case 0x73:  # Image Name
                            self.lineEditPictureName.setText("")
                        case 0x74:  # Image
                            result = []
                            indexImage = 0
                            if self.imageStart: # TRUE
                                indexImage = self.bufferIn[31] + 1
                                print("IndexImage: ", '{:02X}'.format(indexImage))
                                self.lineEditPacket.setText(str(indexImage))
                                self.fileJPG = open(self.pictureFile, "ab")  # append byte to file
                                for k in range(37, 40):
                                    result.append(self.bufferIn[k])
                                # self.pictureHex = self.pictureHex.append(result)
                                self.fileJPG.write(bytes(result))
                                self.fileJPG.close()
                                self.SLSLength = self.SLSLength - 3
        else:
            self.payloadLength = self.bufferIn[7]
            # print("PayloadLength: ", '{:02X}'.format(self.payloadLength))
            match self.PADDataType:
                case 0x80:
                    if self.payloadLength > 1:
                        # print("DLSType: ", '{:02X}'.format(self.DLSType))
                        # print("DLSLength: ", '{:02X}'.format(self.DLSLength))
                        match self.DLSType:
                            case 0x00:
                                if self.DLSLength > 32:
                                    for var in range(8, 40):
                                        self.dynamicLabel = self.dynamicLabel + chr(self.bufferIn[var])
                                    self.DLSLength = self.DLSLength - 32
                                else:
                                    for var in range(8, self.DLSLength + 8):
                                        self.dynamicLabel = self.dynamicLabel + chr(self.bufferIn[var])
                            case 0x80:
                                if self.DLSLength > 32:
                                    for var in range(8, 40):
                                        self.dynamicLabel = self.dynamicLabel + chr(self.bufferIn[var])
                                    self.DLSLength = self.DLSLength - 32
                                else:
                                    for var in range(8, self.DLSLength + 8):
                                        self.dynamicLabel = self.dynamicLabel + chr(self.bufferIn[var])
                case 0x7C:
                    if self.payloadLength > 2:
                        print("MOTSLSType2: ", '{:02X}'.format(self.MOTSLSType))
                        match self.MOTSLSType:
                            case 0x73:
                                for var in range(20, 28):
                                    pictureName = pictureName + chr(self.bufferIn[var])
                                self.lineEditPictureName.setText(pictureName)
                                print("------------------------ Picture Name: ", pictureName)
                                self.loadingPicture()
                                self.imageStart = True
                                self.pictureFile = pictureName
                                # Open a new Image or erase an old Image
                                self.fileJPG = open(self.pictureFile, "wb")
                                self.fileJPG.close()
                            case 0x74:
                                if self.imageStart:
                                    result = []
                                    # append bytes to file
                                    self.fileJPG = open(self.pictureFile, "ab")
                                    if self.SLSLength > 32:
                                        for k in range(8, 40):
                                            result.append(self.bufferIn[k])
                                        self.SLSLength = self.SLSLength - 32
                                        self.fileJPG.write(bytes(result))
                                    else:
                                        for k in range(8, self.SLSLength + 8):
                                            result.append(self.bufferIn[k])
                                        self.fileJPG.write(bytes(result))
                                    self.fileJPG.close()


    def timerArtistTitleTick(self):
        """
        Timer Artist Title Tick
        """
        self.timerArtistTitle.stop()
        if self.checkBoxArtistTitle.isChecked():
            self.softLabelsArtistTitle()
        else:
            self.lineEditArtistDLS.setText(self.dynamicLabel)

    def softLabelsArtistTitle(self):
        """
        Soft Labels Artist Title
        """
        dlsLen = len(self.dynamicLabel)
        charPosition = self.dynamicLabel.find(" - ", 0, dlsLen)
        print(charPosition)
        if charPosition != 0:
            self.title = self.dynamicLabel[0: charPosition]
            self.artist = self.dynamicLabel[charPosition + 2: dlsLen]
            self.lineEditArtistDLS.setText(self.artist)
            self.lineEditTitle.setText(self.title)
        else:
            self.lineEditArtistDLS.setText(self.dynamicLabel)


    def loadingPicture(self):
        """
        Loading Picture
        input = ['0x1', '0x3', '0x2', '0x0', '0x0', '0x10', '0x4', '0x0', '0x0', '0xfa', '0x4']
        result = bytes([int(x,0) for x in input])
        b'\x01\x03\x02\x00\x00\x10\x04\x00\x00\xfa\x04'

        """
        print("Load Picture ...")
        if self.pictureHex != "":
            self.imageStart = False
            fileName = self.pictureFile
            image = QImage()
            # file = QFile()
            pictureByte = QByteArray()
            pictureByte = bytes([int(x, 0) for x in self.pictureHex])
            image.loadFromData(pictureByte)
            suffix = "jpg"
            # options = QFileDialog.options
            # options |= QFileDialog.Option.DontUseNativeDialog
            filename, _ = QFileDialog.getSaveFileName(self, "Save the file", "", "Image (*.jpg)")
            if filename:
                self.image.save(filename, suffix, -1)
            else:
                msgBoxImage = QMessageBox()
                msgBoxImage.setWindowTitle("ERROR FILE IMAGE")
                msgBoxImage.setText("Can't save the file")
                msgBoxImage.setStandardButtons(QMessageBox.StandardButton.Ok)
                if msgBoxImage.exec() == QMessageBox.StandardButton.Ok:
                    pass
            pixmap = QPixmap("picture.jpg")
            self.labelPicture.setPixmap(pixmap)
            self.pictureHex = ""


    def dabGetTime(self):
        """
        DAB Get Time
        if response begins 0xBC
        """
        # print("DAB Get Time")
        year = self.bufferIn[9] * 256 + self.bufferIn[8]
        months = self.bufferIn[10]
        days = self.bufferIn[11]
        hours = self.bufferIn[12]
        minutes = self.bufferIn[13]
        seconds = self.bufferIn[14]
        # date = QDate(year, months, days).toString(Qt.ISODate)
        date = QDate(year, months, days).toString("d MMMM yyyy")
        time = QTime(hours, minutes, seconds).toString()
        dateTime = "Date: " + date + "  Time: " + time
        self.lineEditDateTime.setText(dateTime)
        # print(dateTime)

    def dabGetAudioInfo(self):
        """
        DAB Get Audio Info
        If response 0xBD
        """
        bitRate = self.bufferIn[9] * 256 + self.bufferIn[8]
        self.labelBitRate.setText("Bit Rate: " + str(bitRate) + " kbps")
        sampleRate = (self.bufferIn[11] * 256 + self.bufferIn[10]) / 1000
        self.labelSampleRate.setText("Sample Rate: " + str(sampleRate) + " kHz")

    def dabGetServiceInfo(self):
        """
        DAB Get Service Info
        If response  0xC0
        """
        # currentService = radio name
        currentService = chr(self.bufferIn[12]) + chr(self.bufferIn[13]) + chr(self.bufferIn[14]) \
                         + chr(self.bufferIn[15]) + chr(self.bufferIn[16]) + chr(self.bufferIn[17]) \
                         + chr(self.bufferIn[18]) + chr(self.bufferIn[19]) + chr(self.bufferIn[20]) \
                         + chr(self.bufferIn[21]) + chr(self.bufferIn[22]) + chr(self.bufferIn[23]) \
                         + chr(self.bufferIn[24]) + chr(self.bufferIn[25]) + chr(self.bufferIn[26]) \
                         + chr(self.bufferIn[27]) + chr(self.bufferIn[27])
        self.lineEditCurrentService.setText(currentService)

    def serviceListNotAvailable(self):
        """
        Service List Not Available
        If response : 0xFF
        """
        msgBox2 = QMessageBox()
        msgBox2.setWindowTitle("DAB ERROR")
        msgBox2.setText("Service List is not available !!!")
        msgBox2.setInformativeText("Check your antenna or start a new scan.")
        msgBox2.setStandardButtons(QMessageBox.StandardButton.Ok)
        if msgBox2.exec() == QMessageBox.StandardButton.Ok:
            pass
        else:
            pass

    def tuningForNewEnsemble(self):
        """
        tuning For New Ensemble
        """
        # print("Tuning a new ensemble")
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
        self.timerNewEnsemble.start(300)

    def timerNewEnsembleTick(self):
        """
        Timer New Ensemble Tick
        """
        print("Tick for New Ensemble")
        if self.ensemble.getProgressBarValue() == 100:
            self.timerNewEnsemble.stop()
            self.ensemble.close()

    def loadServices(self):
        """
        Load Services
        """
        if nbServices != 0 :
            for row in range(0, nbServices):
                self.tableWidgetViewServices.setItem(row, 0, QTableWidgetItem(services[row].serviceName))
                self.tableWidgetViewServices.setItem(row, 1, QTableWidgetItem(services[row].serviceID))
                self.tableWidgetViewServices.setItem(row, 2, QTableWidgetItem(services[row].componentID))
                self.tableWidgetViewServices.setItem(row, 3, QTableWidgetItem(services[row].tuneIndex))
                self.tableWidgetViewServices.setItem(row, 4, QTableWidgetItem(services[row].tuneFrequency))
                self.tableWidgetViewServices.setItem(row, 5, QTableWidgetItem(services[row].EID))
                self.tableWidgetViewServices.setItem(row, 6, QTableWidgetItem(services[row].componentLabel))
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
        ***** WORK IN PROGRESS *****
        return: row
        """
        # print("Set Data Services")
        # print("\n")
        row = self.tableWidgetViewServices.currentRow()
        # print(row)
        self.currentIndex = row
        self.startService()

    def startService(self):
        """
        Start the selected service on data grid panel or presets panel

        """
        row = self.currentIndex
        self.bufferOut[1] = 0x81
        self.bufferOut[2] = 0x00
        tuneIndex = int(services[row].tuneIndex, 16)
        self.bufferOut[3] = tuneIndex
        # print(tuneIndex)
        self.bufferOut[4] = 0x00

        serviceID = int(services[row].serviceID, 16)
        self.bufferOut[8] = int((serviceID & 4278190080) / 16777216)
        self.bufferOut[7] = int((serviceID & 16711680) / 65536)
        self.bufferOut[6] = int((serviceID & 65280) / 256)
        self.bufferOut[5] = serviceID & 255

        componentID = int(services[row].componentID, 16)
        self.bufferOut[12] = int((componentID & 4278190080) / 16777216)
        self.bufferOut[11] = int((componentID & 16711680) / 65536)
        self.bufferOut[10] = int((componentID & 65280) / 256)
        self.bufferOut[9] = componentID & 255

        self.hidToSend = True
        self.hidSendCheck()
        """
        dataOut = ' '.join('{:02X}'.format(a) for a in self.bufferOut)
        self.lineEditBufferOut.setText(dataOut)
        order = bytes(bytearray(self.bufferOut))
        self.hidSend(order)
        # print("HID send", order)
        """

    def buttonScanClick(self):
        """
        Button Scan Click
        Scan
        **** WORK IN PROGRESS *****
        """
        # print("Button Scan is clicked")

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
        """
        dataOut = ' '.join('{:02X}'.format(a) for a in self.bufferOut)
        self.lineEditBufferOut.setText(dataOut)
        order = bytes(bytearray(self.bufferOut))
        self.hidSend(order)
        """

# PRESETS DAB+ RADIO



    def presetsButtonDisabled(self):
        """
        All presets buttons are disabled
        """
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
        
        # All presets buttons are enabled
        
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


    def checkBoxMemoryChecked(self):
        """
        Check the checkBoxMemory. If checked, a new service must be loaded
        """
        if self.checkBoxMemory.isChecked():
            print("Memory is checked")
            self.presetsButtonEnabled()
        else:
            print("Memory is not checked")

    def resetPresets(self):
        """
        Reset all presets
        """
        if self.checkBoxMemory.isChecked():
            msgBox6 = QMessageBox()
            msgBox6.setWindowTitle("DAB WARNING")
            msgBox6.setText("Reset all presets")
            msgBox6.setInformativeText("Are you sure?")
            msgBox6.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            answer = msgBox6.exec()
            if answer == QMessageBox.StandardButton.Yes:
                print("Yes")
            if answer == QMessageBox.StandardButton.No:
                print("No")
                pass

    def loadPresets(self):
        """
        Load all presets
        :return:
        """
        self.pushButtonPreset1.setText(presets[0].serviceName.strip())
        self.pushButtonPreset1.setEnabled(presets[0].enable)
        print(presets[0].enable)
        self.pushButtonPreset2.setText(presets[1].serviceName.strip())
        self.pushButtonPreset2.setEnabled(presets[1].enable)
        print(presets[1].enable)
        self.pushButtonPreset3.setText(presets[2].serviceName.strip())
        self.pushButtonPreset3.setEnabled(presets[2].enable)
        self.pushButtonPreset4.setText(presets[3].serviceName.strip())
        self.pushButtonPreset4.setEnabled(presets[3].enable)
        self.pushButtonPreset5.setText(presets[4].serviceName.strip())
        self.pushButtonPreset5.setEnabled(presets[4].enable)
        self.pushButtonPreset6.setText(presets[5].serviceName.strip())
        self.pushButtonPreset6.setEnabled(presets[5].enable)
        self.pushButtonPreset7.setText(presets[6].serviceName.strip())
        self.pushButtonPreset7.setEnabled(presets[6].enable)
        self.pushButtonPreset8.setText(presets[7].serviceName.strip())
        self.pushButtonPreset8.setEnabled(presets[7].enable)
        self.pushButtonPreset9.setText(presets[8].serviceName.strip())
        self.pushButtonPreset9.setEnabled(presets[8].enable)
        self.pushButtonPreset10.setText(presets[9].serviceName.strip())
        self.pushButtonPreset10.setEnabled(presets[9].enable)
        self.pushButtonPreset11.setText(presets[10].serviceName.strip())
        self.pushButtonPreset11.setEnabled(presets[10].enable)
        self.pushButtonPreset12.setText(presets[11].serviceName.strip())
        self.pushButtonPreset12.setEnabled(presets[11].enable)


    def buttonPresetClick(self, index):
        """
        Button Preset Clicked
        :param index: of preset
        """
        match index:
            case 0:
                self.pushButtonPreset1.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = presets[index].serviceID
                self.favorite(serviceID)
            case 1:
                self.pushButtonPreset2.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = presets[index].serviceID
                self.favorite(serviceID)
            case 2:
                self.pushButtonPreset3.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = presets[index].serviceID
                self.favorite(serviceID)
            case 3:
                self.pushButtonPreset4.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = presets[index].serviceID
                self.favorite(serviceID)
            case 4:
                self.pushButtonPreset5.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = presets[index].serviceID
                self.favorite(serviceID)
            case 5:
                self.pushButtonPreset6.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = presets[index].serviceID
                self.favorite(serviceID)
            case 6:
                self.pushButtonPreset7.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = presets[index].serviceID
                self.favorite(serviceID)
            case 7:
                self.pushButtonPreset8.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = presets[index].serviceID
                self.favorite(serviceID)
            case 8:
                self.pushButtonPreset9.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = presets[index].serviceID
                self.favorite(serviceID)
            case 9:
                self.pushButtonPreset10.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = presets[index].serviceID
                self.favorite(serviceID)
            case 10:
                self.pushButtonPreset11.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = presets[index].serviceID
                self.favorite(serviceID)
            case 11:
                self.pushButtonPreset12.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
                serviceID = presets[index].serviceID
                self.favorite(serviceID)
        if self.checkBoxMemory.isChecked():
            print("Memory checked")
            msgBox4 = QMessageBox()
            msgBox4.setWindowTitle("DAB WARNING")
            msgBox4.setText("Add or Modify this preset")
            msgBox4.setInformativeText("Are you sure?")
            msgBox4.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            answer = msgBox4.exec()
            if answer == QMessageBox.StandardButton.Yes:
                print("Yes")
                # currentIndex = self.tableWidgetViewServices.currentRow()
                presets[index].serviceName = services[self.currentIndex].serviceName
                presets[index].serviceID = services[self.currentIndex].serviceID
                presets[index].tuneIndex = services[self.currentIndex].tuneIndex
                presets[index].tuneFrequency = services[self.currentIndex].tuneFrequency
                presets[index].componentID = services[self.currentIndex].componentID
                presets[index].EID = services[self.currentIndex].EID
                presets[index].componentLabel = services[self.currentIndex].componentLabel
                presets[index].enable = True
                """
                presets[index].serviceName = "NEW SERVICE"
                presets[index].serviceID = ""
                presets[index].tuneIndex = ""
                presets[index].tuneFrequency = ""
                presets[index].componentID = ""
                presets[index].EID = ""
                presets[index].componentLabel = ""
                """
                savePresets()
            if answer == QMessageBox.StandardButton.No:
                print("No")
                pass

    def favorite(self, serviceID):
        """
        Search this preset in the services list and start this service

        """
        self.currentIndex = 0
        #
        if nbServices != 0 :
            for row in range(0, nbServices):
                if services[row].serviceID == serviceID :
                    self.currentIndex = row
            print("Current Index: ", self.currentIndex)
            self.startService()



    def checkBoxArtistTitleClick(self):
        """
        Check Box Artist Title Click
        """
        if self.checkBoxArtistTitle.isChecked():
            self.softLabelsArtistTitle()
        else:
            self.lineEditTitle.setText("")
            self.lineEditArtistDLS.setText(self.dynamicLabel)

    def checkBoxMuteClick(self):
        """
        Check Box Mute Click
        Set Mute or not
        """
        self.bufferOut[0] = 0x00
        self.bufferOut[1] = 0x13
        self.bufferOut[2] = 0x00
        self.bufferOut[3] = 0x01
        self.bufferOut[4] = 0x03
        if self.checkBoxMute.isChecked():
            self.bufferOut[5] = 0x03
            # print("Mute")
        else:
            self.bufferOut[5] = 0x00
            # print("Sound active")
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
        """
        dataOut = ' '.join('{:02X}'.format(a) for a in self.bufferOut)
        self.lineEditBufferOut.setText(dataOut)
        order = bytes(bytearray(self.bufferOut))
        self.hidSend(order)
        """

    def checkBoxMonoClick(self):
        """
        Check Box Mono Click
        Set Mono or stereo
        """
        self.bufferOut[0] = 0x00
        self.bufferOut[1] = 0x13
        self.bufferOut[2] = 0x00
        self.bufferOut[3] = 0x02  # Property 0x0302. AUDIO_OUTPUT_CONFIG
        self.bufferOut[4] = 0x03
        if self.checkBoxMono.isChecked():
            self.bufferOut[5] = 0x01
            # print("Mono")
        else:
            self.bufferOut[5] = 0x00
            # print("Stereo")
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
        """
        dataOut = ' '.join('{:02X}'.format(a) for a in self.bufferOut)
        self.lineEditBufferOut.setText(dataOut)
        order = bytes(bytearray(self.bufferOut))
        self.hidSend(order)
        """

    def hScrollBarVolumeValueChanged(self):
        """
        HScrollBar Volume Value Changed and Volume
        """
        self.volume()

    def volume(self):
        """
        Volume
        Change the volume
        """
        # self.labelVolume = str(self.horizontalScrollBarVolume.value())
        self.bufferOut[0] = 0x00
        self.bufferOut[1] = 0x13
        self.bufferOut[2] = 0x00
        self.bufferOut[3] = 0x00
        self.bufferOut[4] = 0x03  # Property 0x0300. AUDIO_ANALOG_VOLUME
        self.bufferOut[5] = self.horizontalScrollBarVolume.value()
        # print("Volume: " + str(self.horizontalScrollBarVolume.value()))
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
        # self.hidSend()
        """
        dataOut = ' '.join('{:02X}'.format(a) for a in self.bufferOut)
        self.lineEditBufferOut.setText(dataOut)
        order = bytes(bytearray(self.bufferOut))
        self.hidSend(order)
        """

    def hidSendCheck(self):
        """
        Timer HID Send Tick

        """
        print("Check HID to send: ")
        if self.hidToSend:  # True
            print("True")
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
                self.pictureHex = ""
        else:
            print("False")
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
        except Exception:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Message")
            msgBox.setText("Writing error")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Cancel)
            msgBox.setDefaultButton(QMessageBox.StandardButton.Cancel)
            answer = msgBox.exec()
            if answer == QMessageBox.StandardButton.Cancel:
                pass

    def test1(self):
        print("Test 1")
        # test DateTime
        # BC 81 80 00 C0 00 00 00 E7 07 05 0E 0A 04 25 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        self.bufferIn = [0xBC, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x00, 0x00, 0xE7, 0x07, 0x05, 0x0E, 0x0A, 0x04, 0x25,
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.dabGetTime()

    def test2(self):
        print("Test2")
        # test Audio Info
        # BD 81 80 00 C0 00 00 00 58 00 80 BB 26 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        self.bufferIn = [0xBD, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x00, 0x00, 0x58, 0x00, 0x80, 0xBB, 0x26, 0x00,
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.dabGetAudioInfo()

    def test3(self):
        print("Test3")
        # test Service Info
        # C0 81 80 00 C0 00 00 00 00 01 00 00 54 53 46 20 4A 41 5A 5A 20 20 20 20 20 20 20 20 00 FF 00 00 00 00 00 00 00 00 00 00
        self.bufferIn = [0xC0, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x54, 0x53,
                         0x46, 0x20, 0x4A, 0x41, 0x5A, 0x5A, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
                         0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.dabGetServiceInfo()

    def test4(self):
        print("Test4")
        # test Service list is not available
        # FF 81 ....
        self.bufferIn = [0xFF, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x54, 0x53,
                         0x46, 0x20, 0x4A, 0x41, 0x5A, 0x5A, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
                         0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.serviceListNotAvailable()

    def test5(self):
        print("Test5")
        # test
        print("Pass 1")
        try:
            self.bufferIn = [0x84, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x00, 0x20, 0x01, 0x00, 0x03, 0x80, 0x23, 0xF2,
                             0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2F, 0x00, 0x00, 0x00, 0x00, 0x00,
                             0x00, 0x00, 0x4C, 0x45, 0x41, 0x4E, 0x20, 0x4F, 0x4E, 0x20, 0x4D, 0x45]
            if self.bufferIn:
                dataInHex = ' '.join('{:02X}'.format(a) for a in self.bufferIn)
                self.lineEditBufferIn.setText(dataInHex)
                print(dataInHex)
                print(self.dataAddress)
                self.getDigitalServiceData()
        except Exception:
            pass
        print("Pass 2")
        try:
            self.bufferIn = [0x84, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x01, 0x20, 0x20, 0x2D, 0x20, 0x54, 0x48, 0x4F,
                             0x4D, 0x41, 0x53, 0x20, 0x45, 0x4E, 0x48, 0x43, 0x4F, 0x20, 0x2F, 0x20, 0x53, 0x54,
                             0x45, 0x50, 0x48, 0x41, 0x4E, 0x45, 0x20, 0x4B, 0x45, 0x52, 0x45, 0x43]
            if self.bufferIn:
                dataInHex = ' '.join('{:02X}'.format(a) for a in self.bufferIn)
                self.lineEditBufferIn.setText(dataInHex)
                print(dataInHex)
                print(self.dataAddress)
                self.getDigitalServiceData()
        except Exception:
            pass
        print("Pass 3")
        try:
            self.bufferIn = [0x84, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x02, 0x03, 0x4B, 0x49, 0x00, 0x54, 0x48, 0x4F,
                             0x4D, 0x41, 0x53, 0x20, 0x45, 0x4E, 0x48, 0x43, 0x4F, 0x20, 0x2F, 0x20, 0x53, 0x54,
                             0x45, 0x50, 0x48, 0x41, 0x4E, 0x45, 0x20, 0x4B, 0x45, 0x52, 0x45, 0x43]
            if self.bufferIn:
                dataInHex = ' '.join('{:02X}'.format(a) for a in self.bufferIn)
                self.lineEditBufferIn.setText(dataInHex)
                print(dataInHex)
                print(self.dataAddress)
                self.getDigitalServiceData()
        except Exception:
            pass
        print("Pass 4")
        try:
            self.bufferIn = [0x84, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x00, 0x1E, 0x01, 0x00, 0x03, 0x80, 0x23, 0xF2,
                             0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00,
                             0x12, 0x00, 0x05, 0x01, 0x00, 0x09, 0x04, 0x0D, 0x1E, 0x00, 0x00, 0x00]
            if self.bufferIn:
                dataInHex = ' '.join('{:02X}'.format(a) for a in self.bufferIn)
                self.lineEditBufferIn.setText(dataInHex)
                print(dataInHex)
                print(self.dataAddress)
                self.getDigitalServiceData()
        except Exception:
            pass

    def test6(self):
        print("Test6")
        # test

    def test7(self):
        print("Test 7")
        # test Image jpg name
        #
        print("Pass 1")
        # 84 81 80 00 C0 00 00 20 01 00 03[7C]23 F2 00 00 04 00 00 00 02 00[22 00]00 00 00 00[73]80 80 00 12 06 5D 00 17 00 02 E6
        # 0x7C = SLS  0x73 = Image_Name
        self.bufferIn = [0x84, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x00, 0x20, 0x01, 0x00, 0x03, 0x7C, 0x23, 0xF2,
                         0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x02, 0x00, 0x22, 0x00, 0x00, 0x00, 0x00, 0x00,
                         0x73, 0x80, 0x80, 0x00, 0x12, 0x06, 0x5D, 0x00, 0x17, 0x00, 0x02, 0xE6]
        dataInHex = ' '.join('{:02X}'.format(a) for a in self.bufferIn)
        self.lineEditBufferIn.setText(dataInHex)
        print(dataInHex)
        print(self.dataAddress)
        self.getDigitalServiceData()
        print("Pass 2")
        # 84 81 80 00 C0 00 01 16 10 0B 84 01 85 00 00 00 00 CC 09 00[31 36 32 39 2E 6A 70 67]B0 4A 80 00 12 06 5D 00 17 00 02 E6
        # 0x31 .. 0x67 = "1629.jpg"
        self.bufferIn = [0x84, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x01, 0x16, 0x10, 0x0B, 0x84, 0x01, 0x85, 0x00,
                         0x00, 0x00, 0x00, 0xCC, 0x09, 0x00, 0x31, 0x36, 0x32, 0x39, 0x2E, 0x6A, 0x70, 0x67,
                         0xB0, 0x4A, 0x80, 0x00, 0x12, 0x06, 0x5D, 0x00, 0x17, 0x00, 0x02, 0xE6]
        dataInHex = ' '.join('{:02X}'.format(a) for a in self.bufferIn)
        self.lineEditBufferIn.setText(dataInHex)
        print(dataInHex)
        print(self.dataAddress)
        self.getDigitalServiceData()

    def test8(self):
        print("Test8")
        # Test Read picture
        pass

    def test9(self):
        print("Image test")

        # Erase picture file
        self.fileJPG = open("picture.jpg", "w")
        self.fileJPG.close()

        # Open text file to display
        fileTXT = open("Debug/DAB_Picture1.txt", "r")

        bufferLine = fileTXT.readlines()

        length = len(bufferLine)

        print("Length of this picture: ", length)

        for line in range(0, length):
            print("Line: ", line, " - ", bufferLine[line])
            codestr = bufferLine[line]
            # self.bufferIn.clear()
            # self.bufferIn[:] = []
            bufferCol = []
            bufferCol.clear()
            for col in range(0, 40):
                code = "0x" + codestr[col * 3: col * 3 + 2]
                bufferCol.append(int(code, 16))

            self.bufferIn = [bufferCol[0], bufferCol[1], bufferCol[2], bufferCol[3], bufferCol[4],
                             bufferCol[5], bufferCol[6], bufferCol[7], bufferCol[8], bufferCol[9],
                             bufferCol[10], bufferCol[11], bufferCol[12], bufferCol[13], bufferCol[14],
                             bufferCol[15], bufferCol[16], bufferCol[17], bufferCol[18], bufferCol[19],
                             bufferCol[20], bufferCol[21], bufferCol[22], bufferCol[23], bufferCol[24],
                             bufferCol[25], bufferCol[26], bufferCol[27], bufferCol[28], bufferCol[29],
                             bufferCol[30], bufferCol[31], bufferCol[32], bufferCol[33], bufferCol[34],
                             bufferCol[35], bufferCol[36], bufferCol[37], bufferCol[38], bufferCol[39]]
            dataInHex = ' '.join('{:02X}'.format(a) for a in self.bufferIn)
            # print("Data Index: ", dataInHex)
            # print("Data Addr.: ", self.dataAddress)
            # Go to this program
            self.getDigitalServiceData()

        # Display the picture
        print("Picture displaying")
        pixmap = QPixmap(self.pictureFile)
        self.labelPicture.setPixmap(pixmap)

    def test10(self):
        print("Test10")
        # test

def main():
    """Main program"""
    app = QApplication(sys.argv)
    window = Dab()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
