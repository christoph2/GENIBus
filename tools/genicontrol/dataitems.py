#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2016 by Christoph Schueler <github.com/Christoph2,
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
    'COMMANDS', 'MEASUREMENT_VALUES', 'REFERENCES', 'PARAMETER', 'STRINGS', 'SIXTEENBIT_MEASUREMENT_VALUES',
    'DATAITEMS', 'defs.ACC_RO', 'defs.ACC_WO', 'defs.ACC_WR'
]

from collections import namedtuple
import yaml

from genilib.utils import createStringBuffer
import genicontrol.defs as defs
from genilib.configuration import readConfigFile

Dataitem = namedtuple('Dataitem', 'name klass id access note')

DATAITEMS = yaml.load(createStringBuffer(readConfigFile("genicontrol", "dataitemsMAGNA.yaml")))

def addToDict(d, k, v):
    d[k] = v

PROTOCOL_DATA = dict()
COMMANDS = dict()
MEASUREMENT_VALUES = dict()
REFERENCES = dict()
PARAMETER = dict()
STRINGS = dict()
SIXTEENBIT_MEASUREMENT_VALUES = dict()


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
    elif item.klass == 11:
        addToDict(SIXTEENBIT_MEASUREMENT_VALUES, item.name, item)

DATAITEMS_FOR_CLASS = {
    defs.APDUClass.PROTOCOL_DATA:               PROTOCOL_DATA,
    defs.APDUClass.MEASURED_DATA:               MEASUREMENT_VALUES,
    defs.APDUClass.COMMANDS:                    COMMANDS,
    defs.APDUClass.CONFIGURATION_PARAMETERS:    PARAMETER,
    defs.APDUClass.REFERENCE_VALUES:            REFERENCES,
    defs.APDUClass.ASCII_STRINGS:               STRINGS,
    defs.APDUClass.SIXTEENBIT_MEASURED_DATA:    SIXTEENBIT_MEASUREMENT_VALUES
}

dataItemsById = lambda klass : dict([(v[2], (k, v[3], v[4])) for k, v in DATAITEMS_FOR_CLASS[klass].items()])
dataItemsByName = lambda klass : dict([(k, (v[2], v[3], v[4])) for k, v in DATAITEMS_FOR_CLASS[klass].items()])

DATAITEMS_BY_ID = {
    defs.APDUClass.PROTOCOL_DATA:               dataItemsById(defs.APDUClass.PROTOCOL_DATA),
    defs.APDUClass.MEASURED_DATA:               dataItemsById(defs.APDUClass.MEASURED_DATA),
    defs.APDUClass.COMMANDS:                    dataItemsById(defs.APDUClass.COMMANDS),
    defs.APDUClass.CONFIGURATION_PARAMETERS:    dataItemsById(defs.APDUClass.CONFIGURATION_PARAMETERS),
    defs.APDUClass.REFERENCE_VALUES:            dataItemsById(defs.APDUClass.REFERENCE_VALUES),
    defs.APDUClass.ASCII_STRINGS:               dataItemsById(defs.APDUClass.ASCII_STRINGS),
    defs.APDUClass.SIXTEENBIT_MEASURED_DATA:    dataItemsById(defs.APDUClass.SIXTEENBIT_MEASURED_DATA)
}

DATAITEMS_BY_NAME = {
    defs.APDUClass.PROTOCOL_DATA:               dataItemsByName(defs.APDUClass.PROTOCOL_DATA),
    defs.APDUClass.MEASURED_DATA:               dataItemsByName(defs.APDUClass.MEASURED_DATA),
    defs.APDUClass.COMMANDS:                    dataItemsByName(defs.APDUClass.COMMANDS),
    defs.APDUClass.CONFIGURATION_PARAMETERS:    dataItemsByName(defs.APDUClass.CONFIGURATION_PARAMETERS),
    defs.APDUClass.REFERENCE_VALUES:            dataItemsByName(defs.APDUClass.REFERENCE_VALUES),
    defs.APDUClass.ASCII_STRINGS:               dataItemsByName(defs.APDUClass.ASCII_STRINGS),
    defs.APDUClass.SIXTEENBIT_MEASURED_DATA:    dataItemsByName(defs.APDUClass.SIXTEENBIT_MEASURED_DATA)
}


#yaml.dump(DATAITEMS, open(r'C:\Users\christoph303\Documents\Arduino\libraries\Genibus\tools\genicontrol\config\dataitems.yaml', 'w'))

"""
Code Alarm Group Alarm Cause
2  Missing Phase
32 Overvoltage
40 Undervoltage
48 Overload
49 Overcurrent (i_mo)
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

