
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
from genicontrol.crc import Crc

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

    assert(length == len(arr) - 4)
    assert(frame == arr)
    for idx in range(defs.PDU_START, length + 2):
        ch = arr[idx]
        crc.update(ch)
    print hex(crc.get()), hex(utils.makeWord(arr[defs.CRC_HIGH], arr[defs.CRC_LOW]))


def main():
    pass

if __name__ == '__main__':
    main()

