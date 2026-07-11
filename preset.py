#!/usr/bin/python3
# This Python file uses the following encoding: utf-8
# -*- coding: utf-8 -*-

"""
This file defines the Preset class containing:
 - the preset position
 - the service name
 - the service ID
 - the component ID
 - the tune index
 - the tune frequency
 - the EID
 - the component label
"""
class Preset:
    """
         Available services
        ...
    Attributes:


    """

    def __init__(self, position, serviceName, serviceID, componentID, tuneIndex, tuneFrequency, EID, componentLabel):
        """ initializes Service class """
        self.position = position
        self.serviceName = serviceName
        self.serviceID = serviceID
        self.componentID = componentID
        self.tuneIndex = tuneIndex
        self.tuneFrequency = tuneFrequency
        self.EID = EID
        self.componentLabel = componentLabel

