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


from collections import namedtuple
import doctest
import fractions
import os
import unittest
import string
import sys
from genicontrol.units import UnitTable

ValueTuple = namedtuple('ValueTuple', 'header unit range zero value')

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

