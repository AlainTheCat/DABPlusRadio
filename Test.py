


# self.pushButtonTest1.clicked.connect(self.test1)
# self.pushButtonTest2.clicked.connect(self.test2)
# self.pushButtonTest3.clicked.connect(self.test3)
# self.pushButtonTest5.clicked.connect(self.test5)
# self.pushButtonTest6.clicked.connect(self.loadServices)
# self.pushButtonTest7.clicked.connect(self.test7)
# self.pushButtonTest8.clicked.connect(self.test8)
# self.pushButtonTest9.clicked.connect(self.test9)
# self.pushButtonTest10.clicked.connect(self.test10)

def test1(self):
    # print("Test 1")
    # test DateTime
    # BC 81 80 00 C0 00 00 00 E7 07 05 0E 0A 04 25 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    self.bufferIn = [0xBC, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x00, 0x00, 0xE7, 0x07, 0x05, 0x0E, 0x0A, 0x04, 0x25,
                        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    self.dabGetTime()

def test2(self):
    # print("Test2")
    # test Audio Info
    # BD 81 80 00 C0 00 00 00 58 00 80 BB 26 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    self.bufferIn = [0xBD, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x00, 0x00, 0x58, 0x00, 0x80, 0xBB, 0x26, 0x00,
                        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    self.dabGetAudioInfo()

def test3(self):
    """Displays service information."""
    # print("Test Service Info")
    # C0 81 80 00 C0 00 00 00 00 01 00 00 54 53 46 20 4A 41 5A 5A 20 20 20 20 20 20 20 20 00 FF 00 00 00 00 00 00 00 00 00 00
    self.bufferIn = [0xC0, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x54, 0x53,
                        0x46, 0x20, 0x4A, 0x41, 0x5A, 0x5A, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
                        0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    self.dabGetServiceInfo()

def test4(self):
    # print("Test Service list is not available")
    # FF 81 ....
    self.bufferIn = [0xFF, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x54, 0x53,
                        0x46, 0x20, 0x4A, 0x41, 0x5A, 0x5A, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
                        0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    serviceListNotAvailable()

def test5(self):
    # print("Test5")
    # test
    # print("Pass 1")

    self.bufferIn = [0x84, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x00, 0x20, 0x01, 0x00, 0x03, 0x80, 0x23, 0xF2,
                        0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2F, 0x00, 0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x4C, 0x45, 0x41, 0x4E, 0x20, 0x4F, 0x4E, 0x20, 0x4D, 0x45]
    if self.bufferIn:
        dataInHex = ' '.join('{:02X}'.format(a) for a in self.bufferIn)
        self.lineEditBufferIn.setText(dataInHex)
        # print(dataInHex)
        # print(self.dataAddress)
        self.getDigitalServiceData()

    # print("Pass 2")
    self.bufferIn = [0x84, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x01, 0x20, 0x20, 0x2D, 0x20, 0x54, 0x48, 0x4F,
                        0x4D, 0x41, 0x53, 0x20, 0x45, 0x4E, 0x48, 0x43, 0x4F, 0x20, 0x2F, 0x20, 0x53, 0x54,
                        0x45, 0x50, 0x48, 0x41, 0x4E, 0x45, 0x20, 0x4B, 0x45, 0x52, 0x45, 0x43]
    if self.bufferIn:
        dataInHex = ' '.join('{:02X}'.format(a) for a in self.bufferIn)
        self.lineEditBufferIn.setText(dataInHex)
        # print(dataInHex)
        # print(self.dataAddress)
        self.getDigitalServiceData()

    # print("Pass 3")

    self.bufferIn = [0x84, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x02, 0x03, 0x4B, 0x49, 0x00, 0x54, 0x48, 0x4F,
                        0x4D, 0x41, 0x53, 0x20, 0x45, 0x4E, 0x48, 0x43, 0x4F, 0x20, 0x2F, 0x20, 0x53, 0x54,
                        0x45, 0x50, 0x48, 0x41, 0x4E, 0x45, 0x20, 0x4B, 0x45, 0x52, 0x45, 0x43]
    if self.bufferIn:
        dataInHex = ' '.join('{:02X}'.format(a) for a in self.bufferIn)
        self.lineEditBufferIn.setText(dataInHex)
        # print(dataInHex)
        # print(self.dataAddress)
        self.getDigitalServiceData()

    # print("Pass 4")
    self.bufferIn = [0x84, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x00, 0x1E, 0x01, 0x00, 0x03, 0x80, 0x23, 0xF2,
                        0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00,
                        0x12, 0x00, 0x05, 0x01, 0x00, 0x09, 0x04, 0x0D, 0x1E, 0x00, 0x00, 0x00]
    if self.bufferIn:
        dataInHex = ' '.join('{:02X}'.format(a) for a in self.bufferIn)
        self.lineEditBufferIn.setText(dataInHex)
        # print(dataInHex)
        # print(self.dataAddress)
        self.getDigitalServiceData()


def test6(self):
    # print("Test6")
    pass
    # test

def test7(self):
    """Displays the image name."""
    # print("Test Image jpg name")
    # print("Pass 1")
    # 84 81 80 00 C0 00 00 20 01 00 03[7C]23 F2 00 00 04 00 00 00 02 00[22 00]00 00 00 00[73]80 80 00 12 06 5D 00 17 00 02 E6
    # 0x7C = SLS  0x73 = Image_Name
    self.bufferIn = [0x84, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x00, 0x20, 0x01, 0x00, 0x03, 0x7C, 0x23, 0xF2,
                        0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x02, 0x00, 0x22, 0x00, 0x00, 0x00, 0x00, 0x00,
                        0x73, 0x80, 0x80, 0x00, 0x12, 0x06, 0x5D, 0x00, 0x17, 0x00, 0x02, 0xE6]
    dataInHex = ' '.join('{:02X}'.format(a) for a in self.bufferIn)
    self.lineEditBufferIn.setText(dataInHex)
    # print(dataInHex)
    # print(self.dataAddress)
    self.getDigitalServiceData()
    # print("Pass 2")
    # 84 81 80 00 C0 00 01 16 10 0B 84 01 85 00 00 00 00 CC 09 00[31 36 32 39 2E 6A 70 67]B0 4A 80 00 12 06 5D 00 17 00 02 E6
    # 0x31 .. 0x67 = "1629.jpg"
    self.bufferIn = [0x84, 0x81, 0x80, 0x00, 0xC0, 0x00, 0x01, 0x16, 0x10, 0x0B, 0x84, 0x01, 0x85, 0x00,
                        0x00, 0x00, 0x00, 0xCC, 0x09, 0x00, 0x31, 0x36, 0x32, 0x39, 0x2E, 0x6A, 0x70, 0x67,
                        0xB0, 0x4A, 0x80, 0x00, 0x12, 0x06, 0x5D, 0x00, 0x17, 0x00, 0x02, 0xE6]
    dataInHex = ' '.join('{:02X}'.format(a) for a in self.bufferIn)
    self.lineEditBufferIn.setText(dataInHex)
    # print(dataInHex)
    # print(self.dataAddress)
    self.getDigitalServiceData()

def test8(self):
    # print("Test Read picture")
    # Test
    pixmap = QPixmap("skyrock.png")
    self.labelPicture.setPixmap(pixmap)
    pass

def test9(self):
    """Displays a test image."""
    # print("Image test")
    # Erase picture file
    self.fileJPG = open("picture.jpg", "w")
    # self.fileJPG = open("8736.png", "w")
    self.fileJPG.close()
    # Open text file to display
    fileTXT = open("Debug/DAB_Picture1.txt", "r")
    bufferLine = fileTXT.readlines()
    length = len(bufferLine)
    # print("Length of this picture: ", length)

    for line in range(0, length):
        # print("Line: ", line, " - ", bufferLine[line])
        codeString = bufferLine[line]
        bufferCol = []
        bufferCol.clear()
        for col in range(0, 40):
            code = "0x" + codeString[col * 3: col * 3 + 2]
            bufferCol.append(int(code, 16))

        self.bufferIn = [bufferCol[0], bufferCol[1], bufferCol[2], bufferCol[3], bufferCol[4],
                            bufferCol[5], bufferCol[6], bufferCol[7], bufferCol[8], bufferCol[9],
                            bufferCol[10], bufferCol[11], bufferCol[12], bufferCol[13], bufferCol[14],
                            bufferCol[15], bufferCol[16], bufferCol[17], bufferCol[18], bufferCol[19],
                            bufferCol[20], bufferCol[21], bufferCol[22], bufferCol[23], bufferCol[24],
                            bufferCol[25], bufferCol[26], bufferCol[27], bufferCol[28], bufferCol[29],
                            bufferCol[30], bufferCol[31], bufferCol[32], bufferCol[33], bufferCol[34],
                            bufferCol[35], bufferCol[36], bufferCol[37], bufferCol[38], bufferCol[39]]
        # dataInHex = ' '.join('{:02X}'.format(a) for a in self.bufferIn)
        # print("Data Index: ", dataInHex)
        # print("Data Addr.: ", self.dataAddress)
        # Go to this program
        self.getDigitalServiceData()
    # Display the picture
    # print("Picture displaying")
    pixmap = QPixmap(self.pictureFile)
    self.labelPicture.setPixmap(pixmap)

def test10(self):
    # print("Test Save Services List")
    self.saveServicesList()