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
from genicontrol.dissect import dissectPumpStatus, dissectResponse
import genicontrol.dataitems as dataitems
import genicontrol.defs as defs
from genicontrol.simu.Simulator import SimulationServer
from genilib.utils import dumpHex, makeWord


class NullModel(ModelIf.IModel):
    logger = logging.getLogger("GeniControl")
    TYPE = "Simulator"
    SPECIAL_DATAPOINTS = ('act_mode1', 'act_mode2', 'act_mode3', 'contr_source')

    def initialize(self, quitEvent):
        for idx, item in enumerate(DataitemConfiguration['MeasurementValues']):
            key, displayName, unit, controlIdValue, controlIdUnit = item
            ditem = dataitems.MEASUREMENT_VALUES[key]
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
        self.online = False
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
        if resp:
            self._controller.trace(True, resp)
        return resp

    def _transact(self, req):
        """Send a telegram and consume its reply (caller holds '_concurrentAccess')."""
        if not self.connected:
            return None
        self.writeToServer(req)
        return self.readFromServer()

    def connect(self, toDriver = True):
        if toDriver:
            res = self._connection.connect()
            self.connected = res
            if not res:
                self._connection.close()
        else:
            #pdu = apdu.createSetRemotePDU(0x01)
            #self._modelThread.request(pdu)
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
        unitAddress = self.getUnitAddress()
        if unitAddress is None or not self.online:
            self.logger.warning("Not connected, cannot set reference value '%s'." % item)
            return
        self._concurrentAccess.acquire()
        try:
            # ref_rem is only used by the pump in REMOTE mode, so switch to REMOTE in the same
            # telegram (like the original reference telegram 27 09 20 01 03 81 07 05 82 01 53 ...).
            req = apdu.createSetValuesPDU(
                apdu.Header(defs.SD_DATA_REQUEST, unitAddress, 0x01),
                references = [(item, int(value))],
                commands = ['REMOTE']
            )
            self.logger.info("Setting %s = %d (0x%02x), switching pump to REMOTE." % (item, int(value), int(value)))
            self._checkAck(self._transact(req), "set %s" % item)
            # Read the references again, so the display shows what the pump actually uses.
            self.refreshReferences()
        finally:
            self._concurrentAccess.release()

    def setParameterValue(self, item, value):
        pass

    def sendCommand(self, command, refreshReferences = False):
        unitAddress = self.getUnitAddress()
        if unitAddress is None or not self.online:
            self.logger.warning("Not connected, cannot send command '%s'." % command)
            return
        self._concurrentAccess.acquire()
        try:
            self.logger.info("Command requested: %s" % command)
            req = apdu.createSetCommandsPDU(
                apdu.Header(defs.SD_DATA_REQUEST, unitAddress, 0x01),
                [command]
            )
            self._checkAck(self._transact(req), "command %s" % command)
            if refreshReferences:
                self.refreshReferences()
        finally:
            self._concurrentAccess.release()

    def switchToRemote(self, refRem = None):
        """Switch the pump to REMOTE.

        The MAGNA does not use its stored bus setpoint (ref_rem) after a plain REMOTE command
        (it keeps regulating to the local setpoint). So the current ref_rem is sent again,
        together with REMOTE in one telegram (like 'Set Reference Value').
        """
        try:
            refRem = int(refRem)
        except (TypeError, ValueError):
            refRem = None
        if refRem is not None and 0 <= refRem <= 254:
            self.setReferenceValue('ref_rem', refRem)
        else:
            self.sendCommand('REMOTE', refreshReferences = True)

    def refreshReferences(self):
        """Re-read references / r_min / r_max in the next polling cycle."""
        if self._modelThread.getState() == RequestorThread.STATE_OPERATIONAL:
            self._modelThread.setState(RequestorThread.STATE_REQ_PARAM)

    ACK_TEXT = {
        defs.ACK_CLASS_UNKNOWN:     "class unknown",
        defs.ACK_ID_UNKNOWN:        "data item unknown",
        defs.ACK_OPERATION_ILLEGAL: "operation illegal / not allowed in current mode",
    }

    def _checkAck(self, resp, what):
        """Check the acknowledge bits of the pump's reply to a SET telegram."""
        if not resp:
            self.logger.warning("No reply from pump to '%s'." % what)
            self.sendMessage('STATUS', "No reply to '%s'" % what)
            return False
        try:
            reply = dissectResponse(resp)
        except Exception as e:
            self.logger.warning("Invalid reply to '%s': %s" % (what, e))
            return False
        ok = True
        for a in reply.APDUs:
            if a.ack != defs.ACK_OK:
                ok = False
                self.logger.warning("Pump rejected '%s': APDU class %s -> %s." % (
                    what, defs.APDUClass.toString(a.klass), self.ACK_TEXT.get(a.ack, a.ack)))
                self.sendMessage('STATUS', "Pump rejected '%s' (%s)" % (what, self.ACK_TEXT.get(a.ack, a.ack)))
        if ok:
            self.logger.info("Pump acknowledged '%s'." % what)
            self.sendMessage('STATUS', "OK: %s" % what)
        return ok

    def roundValue(self, value):
        return int(math.ceil(value * 100))/100.00

    def updateMeasurements(self, measurements):
        items = list(measurements.items())
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
                info = self.getInfo(defs.APDUClass.MEASURED_DATA, key)
                scalingInfo = getScalingInfo(info)
                key = key[ : key.index('_hi')]
                value_hi = value
                value_lo = measurements[key + '_lo']
                value = makeWord(value_hi, value_lo)
                if key == 'speed': # 0x83 Extended Precision 16bit
                    scaledValue = "%.2f" % self.roundValue(conversion.convertExtended16(value, info.zero, info.range, scalingInfo.factor))
                else:
                    scaledValue = "%.2f" % self.roundValue(conversion.convertForward16(value, info.zero, info.range, scalingInfo.factor))
                msg = "MEASURED_DATA.%s"
                self.sendMessage(msg % key + '_hi', scaledValue)
            elif key.endswith('_16'): # 0x83 Extended Precision 16bit
                info = self.getInfo(defs.APDUClass.SIXTEENBIT_MEASURED_DATA, key)
                scalingInfo = getScalingInfo(info)
                if key == 't_w_16':
                    scaledValue = "%.2f" % self.roundValue(conversion.convertExtended16(value, info.zero, info.range, scalingInfo.factor))
                    scaledValue = "%.2f" % (float(scaledValue) - 273.15) # Kelvin -> Celsius
                else:
                    scaledValue = "%.2f" % self.roundValue(conversion.convertExtended16(value, info.zero, info.range, scalingInfo.factor))
                msg = "SIXTEENBIT_MEASURED_DATA.%s"
                self.sendMessage(msg % key, scaledValue)
            else:
                info = self.getInfo(defs.APDUClass.MEASURED_DATA, key)
                scalingInfo = getScalingInfo(info)
                if value == 0xff:
                    scaledValue = 'n/a'
                else:
                    if (info.head & 0x02) == 2:
                        scaledValue = "%.2f" % self.roundValue(conversion.convertForward8(value, info.zero, info.range, scalingInfo.factor))
                    else:
                        scaledValue = str(value) # Unscaled.
                    msg = "MEASURED_DATA.%s"
                self.sendMessage(msg % key, scaledValue)

    def updateReferences(self, references):
        msg = "REFERENCE_VALUES.%s"
        for key, value in list(references.items()):
            self.sendMessage(msg % key, value)

    def updateParameter(self, parameter):
        items = list(parameter.items())
        msg = "CONFIGURATION_PARAMETERS.%s"
        for key, value in items:
            self.sendMessage(msg % key, value)

    def setOnline(self, online):
        """Pump replies (True) or doesn't reply anymore (False)."""
        self.online = online
        self.sendMessage('LINK', online)

    def setValue(self, group, datapoint, value):
        self._setValueLock.acquire()
        self._valueDict.setdefault(group, dict())[datapoint] = value
        self.sendMessage("%s.%s" % (defs.APDUClass.toString(group), datapoint), value)
        self._setValueLock.release()

    def getValue(self, group, datapoint):
        group = self._valueDict.get(group, None)
        if not group:
            return None
        return group.get(datapoint, None)

    def getUnitAddress(self):
        return self.getValue(defs.APDUClass.CONFIGURATION_PARAMETERS, 'unit_addr')

    def updateInfoDict(self, di):
        for key, value in list(di.items()):
            self._infoDict[key].update(value)
        self.sendMessage('INFO', di)

    def getInfo(self, klass, dp):
        return self._infoDict[klass][dp]


def createDataDictionary():
    ddict = dict()

    # klasses = [x for x in dir(defs.APDUClass) if x.upper() and not x.startswith('__')]
    klasses = list(defs.APDUClass.nameDict.keys())
    for klass in klasses:
        ddict[klass] = {}
    return ddict
