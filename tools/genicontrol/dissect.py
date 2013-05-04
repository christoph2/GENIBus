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

from collections import namedtuple
import logging

import genicontrol.utils as utils
import genicontrol.defs as defs
from genicontrol.crc import Crc, CrcError

logger = logging.getLogger("genicontrol")

## dissecting states.
APDU_HEADER0    = 0
APDU_HEADER1    = 1
APDU_DATA       = 2

APDU = namedtuple('APDU', 'klass ack data')
DissectionResult = namedtuple('DissectionResult', 'sd da sa APDUs')

class ADPUClassNotSupportedError(Exception): pass
class FramingError(Exception): pass

def dissectResponse(frame):
    buf = utils.makeBuffer(frame)
    arr =  utils.makeArray(buf)

    crc = Crc(0xffff)
    actualValue = 0
    sd = arr[defs.START_DELIMITER]
    length = arr[defs.LENGTH]
    da = arr[defs.DESTINATION_ADRESS]
    sa = arr[defs.SOURCE_ADDRESS]
    crc.update(length)
    crc.update(da)
    crc.update(sa)

    dissectingState = APDU_HEADER0
    numberOfDataBytes = 0
    byteCount = 0
    result = []

    if not (length == len(arr) - 4):
        raise FramingError("Frame length doesn't match length byte.")
    for idx in range(defs.PDU_START, length + 2):
        ch = arr[idx]
        crc.update(ch)
        if dissectingState == APDU_HEADER0:
            klass = ch & 0x0f
            if klass not in defs.SUPPORTED_CLASSES:
                # Well, to be precise, these classes are not really documented by the GENIBus spec...
                raise ADPUClassNotSupportedError("APDU class '%u' not supported by GeniControl." % klass)
            dissectingState = APDU_HEADER1
            data = []
        elif dissectingState == APDU_HEADER1:
            numberOfDataBytes = ch & 0x3F
            opAck = (ch & 0xC0) >> 6
            byteCount = numberOfDataBytes
            if byteCount:
                dissectingState = APDU_DATA
            else:
                dissectingState = APDU_HEADER0
                result.append(APDU(klass, opAck, data))
        elif dissectingState == APDU_DATA:
            byteCount -= 1
            data.append(ch)
            if byteCount <= 0:
                dissectingState = APDU_HEADER0
                result.append(APDU(klass, opAck, data))
    frameCrc = utils.makeWord(arr[defs.CRC_HIGH], arr[defs.CRC_LOW])
    if crc.get() != frameCrc:
        raise CrcError("Frame CRC doesn't match calculated CRC.")
    return DissectionResult(sd, da, sa, result)



def dissectPumpStatus(dp, value):
    result = []
    if dp == 'act_mode1':
        operationMode = (value & 0x7)
        controlMode = (value & 0x38) >> 3
        nightReduction = (value & 0x40) >> 6

        result.append(('nightReduction', nightReduction, ))
        if operationMode == 0x00:
            om = 'Start'
        elif operationMode == 0x01:
            om = 'Stop'
        elif operationMode == 0x02:
            om = 'Min'
        elif operationMode == 0x03:
            om = 'Max'
        else:
            logger.info('FIX-ME: operationMode "%u"' % operationMode)

        result.append(('operationMode', om, ))

        if controlMode == 0x00:
            cm = 'Constant Pressure'
        elif controlMode == 0x01:
            cm = 'Proportional Pressure'
        elif controlMode == 0x02:
            cm = 'Constant Frequency'
        elif controlMode == 0x05:
            cm = 'Automatic Setpoint'
        result.append(('controlMode', cm, ))
    elif dp == 'act_mode2':
        temperatureInfluence = value & 0x01
        buttonsOnPump = (value & 0x20) >> 5
        minimumCurve = (value & 0xc0) >> 6
        result.append(('temperatureInfluence', temperatureInfluence))
        result.append(('buttonsOnPump', buttonsOnPump))
        result.append(('minimumCurve', minimumCurve))
    elif dp == 'act_mode3':
        sm = value & 0x07
        if sm == 0:
            systemMode = 'Normal'
        elif sm == 3:
            systemMode = 'Survive'
        elif sm == 4:
            systemMode = 'Alarm Standby'
        else:
            systemMode = '???'
        result.append(('systemMode', systemMode))
        pendingAlarm = (value & 0x08) >> 3
        result.append(('pendingAlarm', pendingAlarm))
        sm = (value & 0x10) >> 4
        sourceMode = 'Local' if sm == 1 else 'Remote'
        result.append(('sourceMode', sourceMode))
    elif dp == 'contr_source':
        cs = (value & 0x0f) >> 4
        if cs == 0b0001:
            contrSource = "Buttons"
        elif cs == 0b0010:
            contrSource = "GENIBus"
        elif cs == 0b0011:
            contrSource = "GENILink"
        elif cs == 0b0100:
            contrSource = "External control"
        else:
            contrSource = 'Buttons' # ???
        result.append(('activeSource', contrSource))
    return result


def main():
    pass

if __name__ == '__main__':
    main()

