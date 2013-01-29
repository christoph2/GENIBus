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

import array
import logging
import genicontrol.dataitems as dataitems
import genicontrol.defs as defs
from genicontrol.crc import calcuteCrc
from genicontrol.utils import bytes, dumpHex

logger = logging.getLogger("genicontrol")


def createAPDUHeader(apdu, klass, operationSpecifier, length):
    apdu.append(klass)
    apdu.append((operationSpecifier << 6) | (length & 0x3F))

def createAPDU(klass, op, datapoints):
    di = dataitems.DATAITEMS_FOR_CLASS[klass]
    result = []
    createAPDUHeader(result, klass, op, len(datapoints) * 2)
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


def createSetValuesPDU(header, parameter = [], references = []):
    if not isinstance(header, Header):
        raise TypeError('Parameter "header" must be of type "Header".')

    length = 2
    pdu = []

    if parameter:
        parameterAPDU = createSetParametersAPDU(parameter)
        length += len(parameterAPDU)

    if references:
        referencesAPDU = createSetReferencesAPDU(references)
        length += len(referencesAPDU)

    pdu.extend([header.startDelimiter, length, header.destAddr, header.sourceAddr])

    if parameter:
        pdu.extend(parameterAPDU)

    if references:
        pdu.extend(referencesAPDU)

    crc = calcuteCrc(pdu)
    pdu.extend(bytes(crc))

    arr = array.array('B', pdu)
    # TODO: arr.tostring() for I/O!
    return arr


def createGetInfoPDU(header, measurements = [], parameter = [], references = []):
    if not isinstance(header, Header):
        raise TypeError('Parameter "header" must be of type "Header".')

    length = 2
    pdu = []

    if measurements:
        measurementsAPDU = createGetInfoAPDU(defs.ADPUClass.MEASURERED_DATA, measurements)
        length += len(measurementsAPDU)

    if parameter:
        parameterAPDU = createGetInfoAPDU(defs.ADPUClass.CONFIGURATION_PARAMETERS, parameter)
        length += len(parameterAPDU)

    if references:
        referencesAPDU = createGetInfoAPDU(defs.ADPUClass.REFERENCE_VALUES, references)
        length += len(referencesAPDU)

    pdu.extend([header.startDelimiter, length, header.destAddr, header.sourceAddr])

    if measurements:
        pdu.extend(measurementsAPDU)

    if parameter:
        pdu.extend(parameterAPDU)

    if references:
        pdu.extend(referencesAPDU)

    crc = calcuteCrc(pdu)
    pdu.extend(bytes(crc))

    arr = array.array('B', pdu)
    # TODO: arr.tostring() for I/O!
    return arr


def createSetCommandsPDU(header, commands):
    if not isinstance(header, Header):
        raise TypeError('Parameter "header" must be of type "Header".')

    length = 2
    pdu = []

    commandsAPDU = createSetCommandsAPDU(commands)
    length += len(commandsAPDU)

    pdu.extend([header.startDelimiter, length, header.destAddr, header.sourceAddr])

    pdu.extend(commandsAPDU)

    crc = calcuteCrc(pdu)
    pdu.extend(bytes(crc))

    arr = array.array('B', pdu)
    # TODO: arr.tostring() for I/O!
    return arr



def createConnectRequestPDU(sourceAddr):
    return createGetValuesPDU(
        Header(defs.SD_DATA_REQUEST, defs.CONNECTION_REQ_ADDR, sourceAddr),
        measurements =  ['unit_family', 'unit_type'],
        protocolData =  ['df_buf_len',  'unit_bus_mode'],
        parameter =     ['unit_addr',   'group_addr']
    )


if __name__ == '__main__':
    print dumpHex(createConnectRequestPDU(0x01))

    print dumpHex(createSetCommandsPDU(Header(defs.SD_DATA_REQUEST, 0x20, 0x04), ['REMOTE', 'START']))

    print dumpHex(createSetValuesPDU(Header(defs.SD_DATA_REQUEST, 0x20, 0x04), references = [('ref_rem', 0xa5, )]))

    print dumpHex(createGetInfoPDU(
        Header(defs.SD_DATA_REQUEST, 0x20, 0x04),
        measurements = ['h', 'q', 'p', 'speed', 'energy_hi'])
    )
