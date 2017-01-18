#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2013 by Christoph Schueler <github.com/Christoph2,
##                                      cpu12.gems@googlemail.com>
##
##  All Rights Reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License along
## with this program; if not, write to the Free Software Foundation, Inc.,
## 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
##
##


import abc
import logging
#from wx.lib.pubsub import Publisher as Publisher
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub as Publisher

DATA_NOT_AVAILABLE = None

class IModel(object):
    __metaclass__ = abc.ABCMeta
    logger = logging.getLogger("GeniControl")

    def __init__(self, waitingPoint, connection):
        #super(IModel, self).__init__(self)
        self._pub = Publisher
        self._waitingPoint = waitingPoint
        self._connection = connection
        #self.initialize()

    def sendMessage(self, topic, data):
        if data:
            self._pub.sendMessage(topic, data)

    def subscribe(self, topic, callback):
        self._pub.subscribe(topic = topic, listener = callback)

    def waitForController(self):
        self._waitingPoint.wait()

    @abc.abstractmethod
    def initialize(self):
        pass

    ## todo: getListOf MeasurementValues, etc.

    @abc.abstractmethod
    def connect(self, *parameters):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass

    @abc.abstractmethod
    def requestMeasurementValues(self):
        pass

    @abc.abstractmethod
    def requestParameters(self):
        pass

    @abc.abstractmethod
    def requestReferences(self):
        pass

    @abc.abstractmethod
    def requestInfo(self):
        pass

    @abc.abstractmethod
    def setReferenceValue(self, item, value):
        pass

    @abc.abstractmethod
    def setParameterValue(self, item, value):
        pass

    @abc.abstractmethod
    def sendCommand(self, command):
        pass

    def dissectResponse(self, resp):
        pass

