#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
__author__  = 'Christoph Schueler'
__version__ = '0.1.0'


import unittest

from genibus.utils import helper


class TestHelpers(unittest.TestCase):

    def testHexDump(self):
        self.assertEqual(helper.hexDump(b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x00'), '0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x00')

def main():
    unittest.main()

if __name__ == '__main__':
    main()



