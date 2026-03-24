#!/usr/bin/env python
"""Hilfsfunktionen fuer Byte-/Wort-Konvertierungen im GENIBus-Kontext."""

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

from collections.abc import Iterable, Sequence


def make_word(byte_high: int, byte_low: int) -> int:
    """Kombiniert High- und Low-Byte zu einem 16-Bit-Wert.

    Args:
        byte_high: Hoeherwertiges Byte.
        byte_low: Niederwertiges Byte.

    Returns:
        int: Zusammengesetzter 16-Bit-Wert.
    """
    return ((byte_high & 0xFF) << 8) | (byte_low & 0xFF)


def hi_byte(word: int) -> int:
    """Liefert das High-Byte eines 16-Bit-Werts.

    Args:
        word: Quellwert.

    Returns:
        int: High-Byte im Bereich 0..255.
    """
    return (word & 0xFF00) >> 8


def lo_byte(word: int) -> int:
    """Liefert das Low-Byte eines 16-Bit-Werts.

    Args:
        word: Quellwert.

    Returns:
        int: Low-Byte im Bereich 0..255.
    """
    return word & 0x00FF


def to_bytes(word: int) -> tuple[int, int]:
    """Zerlegt einen 16-Bit-Wert in `(high, low)`.

    Args:
        word: Quellwert.

    Returns:
        tuple[int, int]: Tupel aus High- und Low-Byte.
    """
    return (hi_byte(word), lo_byte(word))


def make_buffer(values: Iterable[int]) -> memoryview:
    """Erzeugt einen schreibbaren `memoryview` ueber den Eingabewerten.

    Args:
        values: Iterierbare Bytewerte.

    Returns:
        memoryview: Speicheransicht auf einem `bytearray`.
    """
    return memoryview(bytearray(values))


def make_array(buf: Sequence[int]) -> tuple[int, ...]:
    """Konvertiert einen bytelike Puffer in ein unveraenderliches Integer-Tupel.

    Args:
        buf: Eingabepuffer mit Bytewerten.

    Returns:
        tuple[int, ...]: Bytewerte als Tupel.
    """
    return tuple(bytearray(buf))


def dump_hex(values: Iterable[int]) -> list[str]:
    """Formatiert Bytewerte als Hex-Strings.

    Args:
        values: Iterierbare Bytewerte.

    Returns:
        list[str]: Liste wie `['0x27', '0x1']`.
    """
    return [hex(value) for value in values]


def makeWord(bh: int, bl: int) -> int:
    """Legacy-Alias fuer `make_word()`.

    Args:
        bh: Hoeherwertiges Byte.
        bl: Niederwertiges Byte.

    Returns:
        int: Zusammengesetzter 16-Bit-Wert.
    """
    return make_word(bh, bl)


def hiByte(w: int) -> int:
    """Legacy-Alias fuer `hi_byte()`.

    Args:
        w: Quellwert.

    Returns:
        int: High-Byte.
    """
    return hi_byte(w)


def loByte(w: int) -> int:
    """Legacy-Alias fuer `lo_byte()`.

    Args:
        w: Quellwert.

    Returns:
        int: Low-Byte.
    """
    return lo_byte(w)


def toBytes(w: int) -> tuple[int, int]:
    """Legacy-Alias fuer `to_bytes()`.

    Args:
        w: Quellwert.

    Returns:
        tuple[int, int]: High-/Low-Byte-Tupel.
    """
    return to_bytes(w)


def makeBuffer(arr: Iterable[int]) -> memoryview:
    """Legacy-Alias fuer `make_buffer()`.

    Args:
        arr: Iterierbare Bytewerte.

    Returns:
        memoryview: Speicheransicht auf einem `bytearray`.
    """
    return make_buffer(arr)


def makeArray(buf: Sequence[int]) -> tuple[int, ...]:
    """Legacy-Alias fuer `make_array()`.

    Args:
        buf: Eingabepuffer.

    Returns:
        tuple[int, ...]: Bytewerte als Tupel.
    """
    return make_array(buf)


def dumpHex(arr: Iterable[int]) -> list[str]:
    """Legacy-Alias fuer `dump_hex()`.

    Args:
        arr: Iterierbare Bytewerte.

    Returns:
        list[str]: Bytewerte als Hex-Strings.
    """
    return dump_hex(arr)
