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
from genicontrol.units import UnitTable

InfoTuple = namedtuple('InfoTuple', 'header unit range zero')
ScalingTuple = namedtuple('ScalingTuple', 'physEntity factor unit valueInterpretation byteOrder scaleInformationFormat signOfZero')

class MalformedScalingInformationError(Exception): pass

def getScalingInfo(infoTuple):
    header = infoTuple.header
    unit = infoTuple.unit
    if (header & 0xc0) != 0x80:
        raise MalformedScalingInformationError()
    else:
        valueInterpretation = (header & 0x20) >> 5
        byteOrder = (header & 0x10) >> 6
        scaleInformationFormat = (header & 0x03)
        signOfZero = (unit & 0x80) >> 7
        unit &= 0x7f
        ut = UnitTable[unit]
        return ScalingTuple(ut.physEntity, ut.factor, ut.unit, valueInterpretation, byteOrder, scaleInformationFormat, signOfZero)


def convertForward8(x, zero, range, unit):
    return (zero + ((x & 0xff) * (range / 254.0))) * unit


def convertReverse8(x, zero, range, unit):
    return (254.0 / (range * unit)) * ((-zero * unit) + x)


def convertForward16(x, zero, range, unit):
    return (zero + ((x & 0xffff) * (range / (254.0 * 256.0)))) * unit


def convertReverse16(x, zero, range, unit):
    return ((254.0 * 256.0)/ (range * unit)) * ((-zero * unit) + x)


