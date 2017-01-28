#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.1.0"

__copyright__ = """
Grundfos GENIBus Library.

(C) 2007-2017 by Christoph Schueler <github.com/Christoph2,
                                     cpu12.gems@googlemail.com>

 All Rights Reserved

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""


from collections import namedtuple
import enum

##
## GeniBus constants.
##
START_DELIMITER     = 0
LENGTH              = 1
DESTINATION_ADRESS  = 2
SOURCE_ADDRESS      = 3
PDU_START           = 4

CRC_HIGH            = -2
CRC_LOW             = -1

MAX_TELEGRAM_LEN    = 259
MAX_PDU_LEN         = 253
SLAVE_ADDR_OFFSET   = 32
CONNECTION_REQ_ADDR = 254
BROADCAST_ADDR      = 255

SD_DATA_REQUEST     = 0x27
SD_DATA_REPLY       = 0x24
SD_DATA_MESSAGE     = 0x26


class Access(enum.IntEnum):

    RO  = 0x01
    WO  = 0x02
    WR  = 0x03


class ADPUClass(enum.IntEnum):

    PROTOCOL_DATA                       = 0
    BUS_DATA                            = 1
    MEASURERED_DATA                     = 2
    COMMANDS                            = 3
    CONFIGURATION_PARAMETERS            = 4
    REFERENCE_VALUES                    = 5
    TEST_DATA                           = 6
    ASCII_STRINGS                       = 7
    MEMORY_BLOCKS                       = 8
    EMBEDDED_PUDS                       = 9
    DATA_OBJECTS                        = 10
    SIXTEENBIT_MEASURERED_DATA          = 11
    SIXTEENBIT_CONFIGURATION_PARAMETERS = 12
    SIXTEENBIT_REFERENCE_VALUES         = 13


NICE_CLASS_NAMES = {
    ADPUClass.PROTOCOL_DATA:                       "Protocol Data",
    ADPUClass.BUS_DATA:                            "Bus Data",
    ADPUClass.MEASURERED_DATA:                     "Measurered Data",
    ADPUClass.COMMANDS:                            "Commands",
    ADPUClass.CONFIGURATION_PARAMETERS:            "Configuration Parameters",
    ADPUClass.REFERENCE_VALUES:                    "Reference Values",
    ADPUClass.TEST_DATA:                           "Test Data",
    ADPUClass.ASCII_STRINGS:                       "ASCII Strings",
    ADPUClass.MEMORY_BLOCKS:                       "Memory Blocks",
    ADPUClass.EMBEDDED_PUDS:                       "Embedded PDUs",
    ADPUClass.DATA_OBJECTS:                        "Data Objects",
    ADPUClass.SIXTEENBIT_MEASURERED_DATA:          "16Bit Measurered Data",
    ADPUClass.SIXTEENBIT_CONFIGURATION_PARAMETERS: "16Bit Configuration Parameters",
    ADPUClass.SIXTEENBIT_REFERENCE_VALUES:         "16Bit Reference Values",
}


class Operation(enum.IntEnum):

    GET  = 0
    SET  = 2
    INFO = 3


class Acknowledge(enum.IntEnum):

    OK                  = 0
    CLASS_UNKNOWN       = 1
    ID_UNKNOWN          = 2
    OPERATION_ILLEGAL   = 3


CLASS_CAPABILITIES = {
    ADPUClass.PROTOCOL_DATA                       : (Operation.GET, ),
    ADPUClass.BUS_DATA                            : (Operation.GET, ),
    ADPUClass.MEASURERED_DATA                     : (Operation.GET, Operation.INFO),
    ADPUClass.COMMANDS                            : (Operation.SET, Operation.INFO),
    ADPUClass.CONFIGURATION_PARAMETERS            : (Operation.GET, Operation.SET, Operation.INFO),
    ADPUClass.REFERENCE_VALUES                    : (Operation.GET, Operation.SET, Operation.INFO),
    ADPUClass.TEST_DATA                           : (Operation.GET, Operation.SET, ),
    ADPUClass.ASCII_STRINGS                       : (Operation.GET, ),
    ADPUClass.MEMORY_BLOCKS                       : (Operation.GET, Operation.SET, ),
    ADPUClass.EMBEDDED_PUDS                       : (Operation.GET, ),
    ADPUClass.DATA_OBJECTS                        : (Operation.GET, Operation.SET, ),
    ADPUClass.SIXTEENBIT_MEASURERED_DATA          : (Operation.GET, Operation.INFO),
    ADPUClass.SIXTEENBIT_CONFIGURATION_PARAMETERS : (Operation.GET, Operation.SET, Operation.INFO),
    ADPUClass.SIXTEENBIT_REFERENCE_VALUES         : (Operation.GET, Operation.SET, Operation.INFO),
}

class IllegalOperationError(Exception): pass

Item = namedtuple('Item', 'name value info')
Info = namedtuple('Info', 'head unit zero range')

