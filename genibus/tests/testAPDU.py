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

import genibus.gbdefs as defs
import genibus.apdu as apdu

import unittest

class TestAPDUs(unittest.TestCase):

    def toHex(self, arr):
        return [x for x in arr]

    def testConnectRequest(self):
        self.assertEqual(self.toHex(apdu.createConnectRequestPDU(0x01)), [0x27, 0x02, 0xfe, 0x01, 0x7d, 0xec])

    def testSetCommands(self):
        self.assertEqual(self.toHex(apdu.createSetCommandsPDU(apdu.Header(defs.FrameType.SD_DATA_REQUEST, 0x20, 0x01), ['REMOTE', 'START'])),
                         [0x27, 0x06, 0x20, 0x01, 0x03, 0x82, 0x07, 0x06, 0x07, 0xfa])

    def testSetValues(self):
        self.assertEqual(self.toHex(apdu.createSetValuesPDU(apdu.Header(defs.FrameType.SD_DATA_REQUEST, 0x20, 0x01), references = [('ref_rem', 0xa5, )])),
                         [0x27, 0x06, 0x20, 0x01, 0x05, 0x82, 0x01, 0xa5, 0x0f, 0x4c])

    def testGetInfoPDU(self):
        self.assertEqual(self.toHex(apdu.createGetInfoPDU(klass = defs.APDUClass.MEASURED_DATA,
            header = apdu.Header(defs.FrameType.SD_DATA_REQUEST, 0x20, 0x01),
            measurements = ['h', 'q', 'p', 't_w', 'speed_hi', 'energy_hi'])),
        [0x27, 0x0a, 0x20, 0x01, 0x02, 0xc6, 0x25, 0x27, 0x22, 0x3a, 0x23, 0x98, 0x33, 0x5a]
        )

def main():
    unittest.main()

if __name__ == '__main__':
    main()


