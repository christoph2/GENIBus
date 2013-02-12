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
import genicontrol.defs as defs
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
        self._setValueLock = threading.RLock()
        self._valueDict = createDataDictionary()
        self._infoDict = createDataDictionary()
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
        self._controller.trace(False, req)

    def readFromServer(self):
        resp = self._server.read()
        self._controller.trace(True, resp)
        return resp

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

    def requestInfo(self, req):
        #print "INFO-REQ"
        #print dumpHex(req)
        self._modelThread.request(req)

    def setReferenceValue(self, item, value):
        pass

    def setParameterValue(self, item, value):
        pass

    def sendCommand(self, command):
        pass

    def setValue(self, group, datapoint, value):
        self._setValueLock.acquire()
        #print "SetValue - Group: %s DP: % s Value: %s" % (defs.ADPUClass.toString(group), datapoint, value)
        self.sendMessage("%s.%s" % (defs.ADPUClass.toString(group), datapoint), value)
        self._setValueLock.release()

    def updateInfoDict(self, di):
        self._infoDict.update(di)
        # TODO: Notify Controller!!!


def createDataDictionary():
    ddict = dict()

    # klasses = [x for x in dir(defs.ADPUClass) if x.upper() and not x.startswith('__')]
    klasses = defs.ADPUClass.nameDict.keys()
    for klass in klasses:
        ddict[klass] = {}
    return ddict
