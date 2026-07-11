#!/usr/bin/python3
# This Python file uses the following encoding: utf-8
# -*- coding: utf-8 -*-

"""
This file contains the various errors specific to the application.
"""


class UsbHidIOError(Exception):
    def __init__(self, message):
        message = "USB HID Device: Reading or writing error"
        super().__init__(message)

# class PlatformException(Exception):
#     def __init__(self, message):
#         message = "Only Windows or Linux platform"
#         super().__init__(message)
