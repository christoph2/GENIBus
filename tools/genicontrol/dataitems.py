#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2014 by Christoph Schueler <github.com/Christoph2,
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

__all__ = [
    'COMMANDS', 'MEASUREMENT_VALUES', 'REFERENCES', 'PARAMETER', 'STRINGS',
    'DATAITEMS', 'defs.ACC_RO', 'defs.ACC_WO', 'defs.ACC_WR'
]

from collections import namedtuple

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

import yaml
import genicontrol.defs as defs
from genicontrol.configuration import readConfigFile


Dataitem = namedtuple('Dataitem', 'name klass id access note')

DATAITEMS = yaml.load(StringIO.StringIO(readConfigFile("genicontrol", "dataitemsUPE.yaml")))


def addToDict(d, k, v):
    d[k] = v


PROTOCOL_DATA = dict()
COMMANDS = dict()
MEASUREMENT_VALUES = dict()
REFERENCES = dict()
PARAMETER = dict()
STRINGS = dict()


for item in DATAITEMS:
    if item.klass == 0:
        addToDict(PROTOCOL_DATA, item.name, item)
    elif item.klass == 2:
        addToDict(MEASUREMENT_VALUES, item.name, item)
    elif item.klass == 3:
        addToDict(COMMANDS, item.name, item)
    elif item.klass == 4:
        addToDict(PARAMETER, item.name, item)
    elif item.klass == 5:
        addToDict(REFERENCES, item.name, item)
    elif item.klass == 7:
        addToDict(STRINGS, item.name, item)

DATAITEMS_FOR_CLASS = {
    defs.ADPUClass.PROTOCOL_DATA:               PROTOCOL_DATA,
    defs.ADPUClass.MEASURERED_DATA:             MEASUREMENT_VALUES,
    defs.ADPUClass.COMMANDS:                    COMMANDS,
    defs.ADPUClass.CONFIGURATION_PARAMETERS:    PARAMETER,
    defs.ADPUClass.REFERENCE_VALUES:            REFERENCES,
    defs.ADPUClass.ASCII_STRINGS:               STRINGS
}

dataItemsById = lambda klass : dict([(v[2], (k, v[3], v[4])) for k, v in DATAITEMS_FOR_CLASS[klass].items()])
dataItemsByName = lambda klass : dict([(k, (v[2], v[3], v[4])) for k, v in DATAITEMS_FOR_CLASS[klass].items()])

DATAITEMS_BY_ID = {
    defs.ADPUClass.PROTOCOL_DATA:               dataItemsById(defs.ADPUClass.PROTOCOL_DATA),
    defs.ADPUClass.MEASURERED_DATA:             dataItemsById(defs.ADPUClass.MEASURERED_DATA),
    defs.ADPUClass.COMMANDS:                    dataItemsById(defs.ADPUClass.COMMANDS),
    defs.ADPUClass.CONFIGURATION_PARAMETERS:    dataItemsById(defs.ADPUClass.CONFIGURATION_PARAMETERS),
    defs.ADPUClass.REFERENCE_VALUES:            dataItemsById(defs.ADPUClass.REFERENCE_VALUES),
    defs.ADPUClass.ASCII_STRINGS:               dataItemsById(defs.ADPUClass.ASCII_STRINGS),
}

DATAITEMS_BY_NAME = {
    defs.ADPUClass.PROTOCOL_DATA:               dataItemsByName(defs.ADPUClass.PROTOCOL_DATA),
    defs.ADPUClass.MEASURERED_DATA:             dataItemsByName(defs.ADPUClass.MEASURERED_DATA),
    defs.ADPUClass.COMMANDS:                    dataItemsByName(defs.ADPUClass.COMMANDS),
    defs.ADPUClass.CONFIGURATION_PARAMETERS:    dataItemsByName(defs.ADPUClass.CONFIGURATION_PARAMETERS),
    defs.ADPUClass.REFERENCE_VALUES:            dataItemsByName(defs.ADPUClass.REFERENCE_VALUES),
    defs.ADPUClass.ASCII_STRINGS:               dataItemsByName(defs.ADPUClass.ASCII_STRINGS),
}


#yaml.dump(DATAITEMS, open(r'C:\Users\christoph303\Documents\Arduino\libraries\Genibus\tools\genicontrol\config\dataitems.yaml', 'w'))

"""
Code Alarm Group Alarm Cause
2  Missing Phase
32 Overvoltage
40 Undervoltage
48 Overload
49 Overcurrent (i_line, i_dc, i_mo)
51 Blocked motor/pump
56 Underload
57 Dry Running
58 Low Flow
64 Overtemperature
65 Motor Temperature (t_m)
66 Control Electronics Temperature (t_e)
67 Power Converter Temperature (t_m)
68 External Temperature / Water Temperature (t_w)
72 Hardware Fault type 1
73 Hardware Shut Down (HSD)
74 Internal Supply Voltage too high
75 Internal Supply Voltage too low
76 Internal Communication failure
77 Twin Pump Communication failure
152 Add On Module Communication Fault
80 Hardware Fault type 2
83 FE Parameter Area Verification error (EEPROM)
85 BE Parameter Area Verification error (EEPROM)
88 Sensor Fault
89 (Feedback) Sensor 1 signal fault
90 RPM Sensor signal fault
91 Temperature Sensor signal fault
92 (Feedback) Sensor calibration fault
"""

