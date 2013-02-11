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

import threading
import logging
import genicontrol.apdu as apdu
import genicontrol.model.ModelIf as ModelIf
from genicontrol.model.config import DataitemConfiguration
from genicontrol.request import RequestorThread
import genicontrol.dataitems as dataitems
from genicontrol.simu.Simulator import SimulationServer
from genicontrol.utils import dumpHex


class NullModel(ModelIf.IModel):
    logger = logging.getLogger("genicontrol")
    TYPE = "Simulator"

    def initialize(self, quitEvent):
        for idx, item in enumerate(DataitemConfiguration['MeasurementValues']):
            key, displayName, unit, controlIdValue, controlIdUnit = item
            ditem =  dataitems.MEASUREMENT_VALUES[key]
            self.sendMessage('Measurements.%s' % key, ModelIf.DATA_NOT_AVAILABLE)
        self.sendMessage('References', ModelIf.DATA_NOT_AVAILABLE)
        self.dataAvailable = False
        self._quitEvent = quitEvent
        self._server = SimulationServer()
        self._modelThread = RequestorThread(self)
        self._requestQueue = self._modelThread.requestQueue
        self._modelThread.start()
        return self._modelThread

    def quit(self):
        self._quitEvent.set()
        self._modelThread.join()

    def writeToServer(self, req):
        self._server.write(req)

    def readFromServer(self):
        return self._server.read()

    def connect(self, *parameters):
        pdu = apdu.createConnectRequestPDU(0x01)
        self._modelThread.request(pdu)
        #self.request(pdu)
        #print dumpHex(pdu)

    def disconnect(self):
        pass

    def request(self, requ):
        self._requestQueue.put(requ)

    def requestMeasurementValues(self):
        pass

    def requestParameters(self):
        pass

    def requestReferences(self):
        pass

    def requestInfo(self):
        pass

    def setReferenceValue(self, item, value):
        pass

    def setParameterValue(self, item, value):
        pass

    def sendCommand(self, command):
        pass


