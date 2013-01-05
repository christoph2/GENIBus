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

import genicontrol.utils as utils
import genicontrol.defs as defs
from genicontrol.crc import Crc, CrcError

## dissecting states.
APDU_HEADER0    = 0
APDU_HEADER1    = 1
APDU_DATA       = 2


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

    if not (length == len(arr) - 4):
        raise FramingError("Frame length doesn't match length byte.")
    assert(frame == arr)
    for idx in range(defs.PDU_START, length + 2):
        ch = arr[idx]
        crc.update(ch)
        if dissectingState == APDU_HEADER0:
            klass = ch & 0x0f
            if klass not in defs.SUPPORTED_CLASSES:
                raise ADPUClassNotSupportedError("APDU class '%u' not supported by GeniControl." % klass)
            dissectingState = APDU_HEADER1
        elif dissectingState == APDU_HEADER1:
            numberOfDataBytes = ch & 0x3F
            opAck = (ch & 0xC0) >> 6
            byteCount = numberOfDataBytes
            if byteCount:
                dissectingState = APDU_DATA
            else:
                dissectingState = APDU_HEADER0
        elif dissectingState == APDU_DATA:
            byteCount -= 1
            if byteCount <= 0:
                dissectingState = APDU_HEADER0
    frameCrc = utils.makeWord(arr[defs.CRC_HIGH], arr[defs.CRC_LOW])
    if crc.get() != frameCrc:
        raise CrcError("Frame CRC doesn't match calculated CRC.")


def main():
    pass

if __name__ == '__main__':
    main()

