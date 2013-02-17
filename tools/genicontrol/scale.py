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

import logging
import os
import sys
from genicontrol.units import UnitTable
from genicontrol.scaling import getScalingInfo, InfoTuple
from genicontrol.conversion import convertForward8, convertForward16

logger = logging.getLogger("genicontrol")

TestValues = (
    (InfoTuple(0x82, 0x3e, 0x39, 0x00), 0x7a),     # i_rst
    (InfoTuple(0x82, 0x15, 0x64, 0x00), 0x42),     # t_mo
    (InfoTuple(0x82, 0x09, 0xfa, 0x00), 0x3980)    # p_hi / p_lo
)


USAGE = """usage: %s header unit range zero value
    Transform raw values into meaningful representataions.
        *** NOTE: This is a low-level debugging-tool. ***

    unit, range, zero and value are hexadicimal numbers.
    unit, range and zero are obtained from an INFO request.
    value is a regular measurement value.

    e.g.: python ValueCalculator.py

""" % os.path.split(sys.argv[0])[1]

#print USAGE

# UNIT      RANGE   ZERO
#   21      90      10
#   44      120     0

u21 = UnitTable[21]
u44 = UnitTable[44]

#print convertForward8(163, 10, 90, 1)
#print convertForward16(0x10d6, 0, 120, 1)


def argumentsToLower():
    return map(lambda x: string.lower(x), sys.argv[1 :])


def main():
    for info, value in TestValues:
        scaling = getScalingInfo(info)
        print scaling
        if value > 0xff:
            print convertForward16(value, info.zero, info.range, scaling.factor)
        else:
            print convertForward8(value, info.zero, info.range, scaling.factor)

if __name__ == '__main__':
    main()

