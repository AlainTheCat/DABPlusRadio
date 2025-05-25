**************************
*     WORK IN PROGRESS   *
**************************

DAB Radio receiver on USB HID
-----------------------------
This program is build with Python 3.10, PySide6 and QtDesigner
on PyCharm IDE (version 2024.3.1.1)

This program runs on Window and Linux.

Hardware
--------
This Radio receiver device is described in the Elektor magazine.
See: https://www.elektormagazine.fr/labs/dab-fm-digital-radio-with-slideshow

Installation
------------

1 - Install all files into PyCharm IDE project (RadioDAB) with requirements.

1 - Plug the device into a USB port.

2 - Run dab.py on PyCharm
    nota: on Linux you need to allow access to USB HID.

    RadioDAB> sudo chmod 0666 your HID path.

Tools
-----

** Designer **

To change the radio design use these commands on terminal:

    RadioDAB> pyside6-designer dab.ui

    RadioDAB> pyside6-uic dab.ui -o MainWindow.py

** Requirements **

To update requirements.txt use this command on terminal:

    RadioDAB> pip freeze > requirements.txt