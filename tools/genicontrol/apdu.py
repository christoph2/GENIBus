#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2012 by Christoph Schueler <github.com/Christoph2,
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

import array
import logging
import genicontrol.dataitems as dataitems
import genicontrol.defs as defs
from genicontrol.crc import calcuteCrc
from genicontrol.utils import bytes

logger = logging.getLogger("genicontrol")

def createAPDUHeader(apdu, klass, operationSpecifier, length):
    apdu.append(klass)
    apdu.append((operationSpecifier << 6) | (length & 0x3F))

def createAPDU(klass, op, datapoints):
    di = dataitems.DATAITEMS_FOR_CLASS[klass]
    result = []
    createAPDUHeader(result, klass, op, len(datapoints))
    for dp, value in datapoints:
        item = di[dp]
        result.append(item.id)
        result.append(value)
    return result

def createAPDUNoData(klass, op, datapoints):
    di = dataitems.DATAITEMS_FOR_CLASS[klass]
    result = []
    createAPDUHeader(result, klass, op, len(datapoints))
    for dp in datapoints:
        item = di[dp]
        result.append(item.id)
    return result

def createGetInfoAPDU(klass, datapoints):
    result = createAPDUNoData(klass, defs.OS_INFO, datapoints)
    return result

def createGetMeasuredDataAPDU(datapoints):
    result = createAPDUNoData(defs.ADPUClass.MEASURERED_DATA, defs.OS_GET, datapoints)
    return result

def createSetCommandsAPDU(datapoints):
    result = createAPDUNoData(defs.ADPUClass.COMMANDS, defs.OS_SET, datapoints)
    return result

def createGetReferencesAPDU(datapoints):
    result = createAPDUNoData(defs.ADPUClass.REFERENCE_VALUES, defs.OS_GET, datapoints)
    return result

def createSetReferencesAPDU(datapoints):
    result = createAPDU(defs.ADPUClass.REFERENCE_VALUES, defs.OS_SET, datapoints)
    return result

def createGetStringsAPDU(datapoints):
    result = createAPDUNoData(defs.ADPUClass.ASCII_STRINGS, defs.OS_GET, datapoints)
    return result

def createGetParametersAPDU(datapoints):
    result = createAPDUNoData(defs.ADPUClass.CONFIGURATION_PARAMETERS, defs.OS_GET, datapoints)
    return result

def createSetParametersAPDU(datapoints):
    result = createAPDU(defs.ADPUClass.CONFIGURATION_PARAMETERS, defs.OS_SET, datapoints)
    return result

def createGetProtocolDataAPDU(datapoints):
    result = createAPDUNoData(defs.ADPUClass.PROTOCOL_DATA, defs.OS_GET, datapoints)
    return result


class Header(object):
    def __init__(self, startDelimiter, destAddr, sourceAddr):
        self.startDelimiter = startDelimiter
        self.destAddr = destAddr
        self.sourceAddr = sourceAddr


def createGetValuesPDU(header, protocolData = [], measurements = [], parameter = [], references = [], strings = []):
    if not isinstance(header, Header):
        raise TypeError('Parameter "header" must be of type "Header".')

    length = 2
    pdu = []

    if protocolData:
        protocolAPDU = createGetProtocolDataAPDU(protocolData)
        length += len(protocolAPDU)

    if measurements:
        measurementAPDU = createGetMeasuredDataAPDU(measurements)
        length += len(measurementAPDU)

    if parameter:
        parameterAPDU = createGetParametersAPDU(parameter)
        length += len(parameterAPDU)

    if references:
        referencesAPDU = createGetReferencesAPDU(references)
        length += len(referencesAPDU)

    if strings:
        stringsAPDU = createGetStringsAPDU(strings)
        length += len(stringsAPDU )

    pdu.extend([header.startDelimiter, length, header.destAddr, header.sourceAddr])

    if protocolData:
        pdu.extend(protocolAPDU)

    if parameter:
        pdu.extend(parameterAPDU)

    if measurements:
        pdu.extend(measurementAPDU)

    if references:
        pdu.extend(referencesAPDU)

    if strings:
        pdu.extend(stringsAPDU)

    crc = calcuteCrc(pdu)
    pdu.extend(bytes(crc))

    arr = array.array('B', pdu)
    # TODO: arr.tostring() for I/O!
    return arr

from genicontrol.model.config import DataitemConfiguration

# mv = [x[0] for x in DataitemConfiguration['MeasurementValues']]
pd = ['df_buf_len', 'unit_bus_mode']
mv = ['unit_family',  'unit_type']
cp = ['unit_addr', 'group_addr']

apdu = createGetValuesPDU(Header(defs.SD_DATA_REQUEST, defs.CONNECTION_REQ_ADDR, 0x01), measurements = mv, protocolData = pd, parameter = cp)

print [hex(x) for x in apdu]
