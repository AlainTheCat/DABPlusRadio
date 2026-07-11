#!/usr/bin/python3
# This Python file uses the following encoding: utf-8
# -*- coding: utf-8 -*-

"""
This file defines the Service class containing:
 - the service preset indicator:
    0 not selected,
    1, 2, 3 ...: order of selected stations
 - the service name
 - the service ID
 - the component ID
 - the tune index
 - the tune frequency
 - the EID
 - the component label
"""

class Service:
    """
         Available services
        ...
    Attributes:


    """

    def __init__(self, preset, serviceName, serviceID, componentID, tuneIndex, tuneFrequency, EID, componentLabel):
        """ initializes Service class """
        self.preset = preset
        self.serviceName = serviceName
        self.serviceID = serviceID
        self.componentID = componentID
        self.tuneIndex = tuneIndex
        self.tuneFrequency = tuneFrequency
        self.EID = EID
        self.componentLabel = componentLabel
