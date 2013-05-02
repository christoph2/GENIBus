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


import math
import threading
import logging
import genicontrol.apdu as apdu
import genicontrol.model.ModelIf as ModelIf
from genicontrol.model.config import DataitemConfiguration
import genicontrol.conversion as conversion
from genicontrol.request import RequestorThread
from genicontrol.scale import getScalingInfo
from genicontrol.dissect import dissectPumpStatus
import genicontrol.dataitems as dataitems
import genicontrol.defs as defs
from genicontrol.simu.Simulator import SimulationServer
from genicontrol.utils import dumpHex, makeWord


class NullModel(ModelIf.IModel):
    logger = logging.getLogger("genicontrol")
    TYPE = "Simulator"
    SPECIAL_DATAPOINTS = ('act_mode1', 'act_mode2', 'act_mode3', 'contr_source')

    def initialize(self, quitEvent):
        for idx, item in enumerate(DataitemConfiguration['MeasurementValues']):
            key, displayName, unit, controlIdValue, controlIdUnit = item
            ditem =  dataitems.MEASUREMENT_VALUES[key]
            self.sendMessage('Measurements.%s' % key, ModelIf.DATA_NOT_AVAILABLE)
        self.sendMessage('References', ModelIf.DATA_NOT_AVAILABLE)
        self.dataAvailable = False
        self._quitEvent = quitEvent
        self._setValueLock = threading.RLock()
        self._concurrentAccess = threading.Lock()
        self._commandRequested = False
        self._valueDict = createDataDictionary()
        self._infoDict = createDataDictionary()
        self._values = dict()
        self.connected = False
        self._modelThread = RequestorThread(self)
        self._requestQueue = self._modelThread.requestQueue
        self._modelThread.start()
        return self._modelThread

    def quit(self):
        self._quitEvent.set()
        self._modelThread.join()

    def writeToServer(self, req):
        self._connection.write(req)
        self._controller.trace(False, req)

    def readFromServer(self):
        resp = self._connection.read(0x100)
        self._controller.trace(True, resp)
        return resp

    def connect(self, toDriver = True):
        if toDriver:
             res = self._connection.connect()
             self.connected = res
             if not res:
                  self._connection.close()
        else:
             pdu = apdu.createConnectRequestPDU(0x01)
             self._modelThread.request(pdu)

    def disconnect(self):
        pass

    def request(self, requ):
        self._requestQueue.put(requ)

    def requestMeasurementValues(self):
        pass

    def requestParameters(self):
        pass

    def requestReferences(self, req):
        pass

    def requestInfo(self, req):
        self._modelThread.request(req)

    def setReferenceValue(self, item, value):
        pass

    def setParameterValue(self, item, value):
        pass

    def sendCommand(self, command):
        self._concurrentAccess.acquire()
        print "Command requested:", command
        self._commandRequested = True
        req = apdu.createSetCommandsPDU(
            apdu.Header(defs.SD_DATA_REQUEST, self.getUnitAddress(), 0x04),
            [command]
        )
        self.writeToServer(req)
        self._concurrentAccess.release()

    def roundValue(self, value):
        return int(math.ceil(value * 100))/100.00

    def updateMeasurements(self, measurements):
        items = measurements.items()
        for key, value in items:
            if key in NullModel.SPECIAL_DATAPOINTS:
                 # Special handling of bit fields.
                 msg = "PUMP_STATUS.%s"
                 datapoints = dissectPumpStatus(key, value)
                 for key, value in datapoints:
                        self.sendMessage(msg % key, str(value))
            elif key.endswith('_lo'):
                continue
            elif key.endswith('_hi'):
                key = key[ : key.index('_hi')]
                #print "16Bit", key,
                value_hi = value
                value_lo = measurements[key + '_lo']
                value = makeWord(value_hi, value_lo)
                scaledValue = "%.2f" % self.roundValue(conversion.convertForward16(value, info.zero, info.range, scalingInfo.factor))
                msg = "MEASURERED_DATA.%s"
                self.sendMessage(msg % key + '_hi', scaledValue)
            else:
                 info = self.getInfo(defs.ADPUClass.MEASURERED_DATA, key)
                 scalingInfo = getScalingInfo(info)
                 if value == 0xff:
                     scaledValue = 'n/a'
                 else:
                    if (info.head & 0x02) == 2:
                        scaledValue = "%.2f" % self.roundValue(conversion.convertForward8(value, info.zero, info.range, scalingInfo.factor))
                    else:
                        scaledValue = str(value) # Unscaled.
                    msg = "MEASURERED_DATA.%s"
                    self.sendMessage(msg % key, scaledValue)

    def updateReferences(self, references):
        msg = "REFERENCE_VALUES.%s"
        for key, value in references.items():
            self.sendMessage(msg % key, value)

    def updateParameter(self, parameter):
        msg = "CONFIGURATION_PARAMETERS.%s"
        for key, value in parameter.items():
            self.sendMessage(msg % key, value)

    def setValue(self, group, datapoint, value):
        self._setValueLock.acquire()
        #print "SetValue - Group: %s DP: % s Value: %s" % (defs.ADPUClass.toString(group), datapoint, value)
        self._valueDict.setdefault(group, dict())[datapoint] = value
        self.sendMessage("%s.%s" % (defs.ADPUClass.toString(group), datapoint), value)
        self._setValueLock.release()

    def getValue(self, group, datapoint):
        return self._valueDict[group][datapoint]

    def getUnitAddress(self):
        return self.getValue(defs.ADPUClass.CONFIGURATION_PARAMETERS, 'unit_addr')

    def updateInfoDict(self, di):
        for key, value in di.items():
            self._infoDict[key].update(value)
        self.sendMessage('INFO', di)

    def getInfo(self, klass, dp):
        return self._infoDict[klass][dp]


def createDataDictionary():
    ddict = dict()

    # klasses = [x for x in dir(defs.ADPUClass) if x.upper() and not x.startswith('__')]
    klasses = defs.ADPUClass.nameDict.keys()
    for klass in klasses:
        ddict[klass] = {}
    return ddict
