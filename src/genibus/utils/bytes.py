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
__author__ = "Christoph Schueler"
__version__ = "0.1.0"

from typing import Iterable, List, Sequence, Tuple


def make_word(byte_high: int, byte_low: int) -> int:
    return ((byte_high & 0xFF) << 8) | (byte_low & 0xFF)


def hi_byte(word: int) -> int:
    return (word & 0xFF00) >> 8


def lo_byte(word: int) -> int:
    return word & 0x00FF


def to_bytes(word: int) -> Tuple[int, int]:
    return (hi_byte(word), lo_byte(word))


def make_buffer(values: Iterable[int]) -> memoryview:
    return memoryview(bytearray(values))


def make_array(buf: Sequence[int]) -> Tuple[int, ...]:
    return tuple(bytearray(buf))


def dump_hex(values: Iterable[int]) -> List[str]:
    return [hex(value) for value in values]


def makeWord(bh: int, bl: int) -> int:
    return make_word(bh, bl)


def hiByte(w: int) -> int:
    return hi_byte(w)


def loByte(w: int) -> int:
    return lo_byte(w)


def toBytes(w: int) -> Tuple[int, int]:
    return to_bytes(w)


def makeBuffer(arr: Iterable[int]) -> memoryview:
    return make_buffer(arr)


def makeArray(buf: Sequence[int]) -> Tuple[int, ...]:
    return make_array(buf)


def dumpHex(arr: Iterable[int]) -> List[str]:
    return dump_hex(arr)
