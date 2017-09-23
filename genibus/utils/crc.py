#!/usr/bin/env python
# -*- coding: utf-8 -*-

import binascii

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


class CrcError(Exception):
    pass


def calc_raw(_bytes):
    return binascii.crc_hqx(bytearray(_bytes), 0xffff) ^ 0xffff

def append_tel(telegram):
    crc = calc_raw(telegram[1:])
    return telegram + bytearray([crc >> 8, crc & 0xff])

def check_tel(telegram, silent=False):
    telegram = bytearray(telegram)
    match = calc_raw(telegram[1:-2]) == (telegram[-2] << 8) + telegram[-1]
    if not match and not silent:
        raise CrcError('Telegram CRC not match!')
    else:
        return match
