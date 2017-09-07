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


import unittest

from genibus.utils.crc import check_tel

TEST_VECTORS = (
    (0x27, 0x07, 0x20, 0x01, 0x02, 0xC3, 0x02, 0x10, 0x1A, 0x90, 0x1c),
    (0x27, 0x0e, 0xfe, 0x01, 0x00, 0x02, 0x02, 0x03, 0x04, 0x02, 0x2e, 0x2f, 0x02, 0x02, 0x94, 0x95, 0xa2, 0xaa),
    (0x24, 0x0e, 0x01, 0x20, 0x00, 0x02, 0x46, 0x0e, 0x04, 0x02, 0x20, 0xf7, 0x02, 0x02, 0x03, 0x01, 0x00, 0x04),
    (0x24, 0x10, 0x01, 0x20, 0x02, 0x0c, 0x82, 0x3e, 0x00, 0x39, 0x82, 0x15, 0x00, 0x64, 0x82, 0x09, 0x00, 0xfa, 0x91, 0x0a),
    (0x27, 0x0f, 0x20, 0x01, 0x02, 0x04, 0x02, 0x10, 0x1a, 0x1b, 0x04, 0x02, 0x04, 0x05, 0x03, 0x81, 0x06, 0x80, 0x2a),
    (0x24, 0x0e, 0x01, 0x20, 0x02, 0x04, 0x7a, 0x42, 0x39, 0x80, 0x04, 0x02, 0xb5, 0xc8, 0x03, 0x00, 0xf2, 0xd7),
)

class TestCRC(unittest.TestCase):

    def test01(self):
        self.assertTrue(check_tel(TEST_VECTORS[0]))

    def test02(self):
        self.assertTrue(check_tel(TEST_VECTORS[1]))

    def test03(self):
        self.assertTrue(check_tel(TEST_VECTORS[2]))

    def test04(self):
        self.assertTrue(check_tel(TEST_VECTORS[3]))

    def test05(self):
        self.assertTrue(check_tel(TEST_VECTORS[4]))

    def test06(self):
        self.assertTrue(check_tel(TEST_VECTORS[5]))


def main():
    unittest.main()

if __name__ == '__main__':
    main()

