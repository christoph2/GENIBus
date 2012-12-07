#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2012 by Christoph Schueler <github.com/Christoph2,
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


from collections import namedtuple
import doctest
import fractions
import os
import unittest
import string
import sys

ValueTuple = namedtuple('ValueTuple', 'header unit range zero value')
Unit = namedtuple('Unit', 'physEntity factor unit')

UnitTable = {
    1:  Unit(u"Electrical current",  0.1,    u"A"),
    2:  Unit(u"Electrical current",  5,      u"A"),
    3:  Unit(u"Voltage",             0.1,    u"V"),
    4:  Unit(u"Voltage",             1,      u"V"),
    5:  Unit(u"Voltage",             5,      u"V"),
    6:  Unit(u"Elec. resistance",    1,      u"Ω"),
    7:  Unit(u"Power (active)",      1,      u"W"),
    8:  Unit(u"Power (active)",      10,     u"W"),
    9:  Unit(u"Power (active)",      100,    u"W"),

    10: Unit(u"Power (apparent)",    1,      u"VA"),
    11: Unit(u"Power (apparent)",    10,     u"VA"),
    12: Unit(u"Power (apparent)",    100,    u"VA"),
    13: Unit(u"Power (reactive)",    1,      u"VAr"),
    14: Unit(u"Power (reactive)",    10,     u"Var"),
    15: Unit(u"Power (reactive)",    100,    u"VAr"),
    16: Unit(u"Frequency",           1,      u"Hz"),
    17: Unit(u"Frequency",           2.5,    u"Hz"),
    18: Unit(u"Rot. velocity",       12,     u"rpm"),
    19: Unit(u"Rot. velocity",       100,    u"rpm"),

    20: Unit(u"Temperature",         0.1,    u"°C"),
    21: Unit(u"Temperature",         1,      u"°C"),
    22: Unit(u"Flow",                0.1,    u"m³/h"),
    23: Unit(u"Flow",                1,      u"m³/h"),
    24: Unit(u"Head",                0.1,    u"m"),
    25: Unit(u"Head",                1,      u"m"),
    26: Unit(u"Head",                10,     u"m"),
    27: Unit(u"Pressure",            0.01,   u"bar"),
    28: Unit(u"Pressure",            0.1,    u"bar"),
    29: Unit(u"Pressure",            1,      u"bar"),

    30: Unit(u"Percentage",          1,      u"%"),
    31: Unit(u"Energy",              1,      u"kWh"),
    32: Unit(u"Energy",              10,     u"kWh"),
    33: Unit(u"Energy",              100,    u"kWh"),
    34: Unit(u"Ang. velocity",       2,      u"rad/s"),
    35: Unit(u"Time",                1,      u"h"),
    36: Unit(u"Time",                2,      u"min"),
    37: Unit(u"Time",                1,      u"s"),
    38: Unit(u"Frequency",           2,      u"Hz"),
    39: Unit(u"Time",                1024,   u"h"),

    40: Unit(u"Energy",              512,    u"kWh"),
    41: Unit(u"Flow",                5,      u"m³/h"),
    42: Unit(u"Electrical current",  0.2,    u"A"),
    43: Unit(u"Elec. resistance",    10,     u"kΩ"),
    44: Unit(u"Power (active)",      1,      u"kW"),
    45: Unit(u"Power (active)",      10,     u"kW"),
    46: Unit(u"Energy",              1,      u"MWh"),
    47: Unit(u"Energy",              10,     u"MWh"),
    48: Unit(u"Energy",              100,    u"MWh"),
    49: Unit(u"Ang. degrees",        1,      u"°"),

    50: Unit(u"Gain",                1,      u""),
    51: Unit(u"Pressure",            0.001,  u"bar"),
    52: Unit(u"Flow",                1,      u"l/s"),
    53: Unit(u"Flow",                1,      u"m³/s"),
    54: Unit(u"Flow",                1,      u"gpm"),
    55: Unit(u"Pressure",            1,      u"psi"),
    56: Unit(u"Head",                1,      u"ft"),
    57: Unit(u"Temperature",         1,      u"°F"),
    58: Unit(u"Flow",                10,     u"gpm"),
    59: Unit(u"Head",                10,     u"ft"),

    60: Unit(u"Pressure",            10,     u"psi"),
    61: Unit(u"Pressure",            1,      u"kPa"),
    62: Unit(u"Electrical current",  0.5,    u"A"),
    63: Unit(u"Flow",                0.1,    u"l/s"),
    64: Unit(u"Volume",              0.1,    u"m³"),
    65: Unit(u"Volume",              1000,   u"m³"),
    66: Unit(u"Energy pr vol.",      10,     u"kWh/m³"),
    67: Unit(u"Volume",              256,    u"m³"),
    68: Unit(u"Area",                1,      u"m²"),
    69: Unit(u"Flow",                0.1,    u"ml/h"),

    70: Unit(u"Volume",              0.1,    u"ml"),
    71: Unit(u"Volume",              1,      u"nl"),
    72: Unit(u"Time",                1024,   u"min"),
    73: Unit(u"Flow",                0.5,    u"l/h"),
    74: Unit(u"Energy pr vol.",      1,      u"Wh/m³")
}


TestValues = (
    ValueTuple(0x82, 0x3e, 0x39, 0x00, 0x7a),     # i_rst
    ValueTuple(0x82, 0x15, 0x64, 0x00, 0x42),     # t_mo
    ValueTuple(0x82, 0x09, 0xfa, 0x00, 0x3980)    # p_hi / p_lo
)


def analyze(valueTuple):
    header = valueTuple.header
    unit = valueTuple.unit
    if (header & 0xc0) != 0x80:
        print "shit"
    else:
        valueInterpretation = (header & 0x20) >> 5
        byteOrder = (header & 0x10) >> 6
        scaleInformationFormat = (header & 0x03)
        signOfZero = (unit & 0x80) >> 7
        unit &= 0x7f
        ut = UnitTable[unit]
        print "vi: %u bo: %u sif: %u sz: %u" % (valueInterpretation, byteOrder,
            scaleInformationFormat, signOfZero),
        print "Unit:", ut
        unitFactor = ut.factor

        # 'header unit range zero value'
        if valueTuple.value > 0xff:
            print "Value:", ConvertForward16(valueTuple.value, valueTuple.zero, valueTuple.range, unitFactor)
        else:
            print "Value:", ConvertForward8(valueTuple.value, valueTuple.zero, valueTuple.range, unitFactor)


        #return valueInterpretation, byteOrder, scaleInformationFormat, signOfZero, unit


def ConvertForward8(x, zero, range, unit):
    return (zero + ((x & 0xff) * (range / 254.0))) * unit


def ConvertReverse8(x, zero, range, unit):
    return (254.0 / (range * unit)) * ((-zero * unit) + x)


def ConvertForward16(x, zero, range, unit):
    return (zero + ((x & 0xffff) * (range / (254.0 * 256.0)))) * unit


def ConvertReverse16(x, zero, range, unit):
    return ((254.0 * 256.0)/ (range * unit)) * ((-zero * unit) + x)



USAGE = """usage: %s header unit range zero value
    Transform raw values into meaningful representataions.
        *** NOTE: This is a low-level debugging-tool. ***

    unit, range, zero and value are hexadicimal numbers.
    unit, range and zero are obtained from an INFO request.
    value is a regular measurement value.

    e.g.: python ValueCalculator.py

""" % os.path.split(sys.argv[0])[1]

print USAGE

# UNIT      RANGE   ZERO
#   21      90      10
#   44      120     0

u21 = UnitTable[21]
u44 = UnitTable[44]

print ConvertForward8(163, 10, 90, 1)
print ConvertForward16(0x10d6, 0, 120, 1)


def argumentsToLower():
    return map(lambda x: string.lower(x), sys.argv[1 :])


def main():
    for tpl in TestValues:
        analyze(tpl)

if __name__ == '__main__':
    main()

