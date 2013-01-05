
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

import os

##
## Common constants.
##
HOME_DIRECTORY = os.path.abspath(os.path.expanduser('~/'))
CONFIGURATION_DIRECTORY = os.path.join(HOME_DIRECTORY, 'GeniControl')

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

##
## ADPU classes.
##
class ADPUClass:
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

##
## Operation specifiers.
##
OS_GET  = 0
OS_SET  = 2
OS_INFO = 3

##
## Acknowledges.
##
ACK_OK                  = 0
ACK_CLASS_UNKNOWN       = 1
ACK_ID_UNKNOWN          = 2
ACK_OPERATION_ILLEGAL   = 3

##
## Valid operations for ADPU classes.
##
CLASS_CAPABILITIES = {
    ADPUClass.PROTOCOL_DATA                       : (OS_GET, ),
    ADPUClass.BUS_DATA                            : (OS_GET, ),
    ADPUClass.MEASURERED_DATA                     : (OS_GET, OS_INFO),
    ADPUClass.COMMANDS                            : (OS_SET, OS_INFO),
    ADPUClass.CONFIGURATION_PARAMETERS            : (OS_GET, OS_SET, OS_INFO),
    ADPUClass.REFERENCE_VALUES                    : (OS_GET, OS_SET, OS_INFO),
    ADPUClass.TEST_DATA                           : (OS_GET, OS_SET, ),
    ADPUClass.ASCII_STRINGS                       : (OS_GET, ),
    ADPUClass.MEMORY_BLOCKS                       : (OS_GET, OS_SET, ),
    ADPUClass.EMBEDDED_PUDS                       : (OS_GET, ),
    ADPUClass.DATA_OBJECTS                        : (OS_GET, OS_SET, ),
    ADPUClass.SIXTEENBIT_MEASURERED_DATA          : (OS_GET, OS_INFO),
    ADPUClass.SIXTEENBIT_CONFIGURATION_PARAMETERS : (OS_GET, OS_SET, OS_INFO),
    ADPUClass.SIXTEENBIT_REFERENCE_VALUES         : (OS_GET, OS_SET, OS_INFO),
}

