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

import logging
import genicontrol.dataitems as dataitems
import genicontrol.defs as defs

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

class APDUBuilder(object):
    def __init__(self):
        pass

