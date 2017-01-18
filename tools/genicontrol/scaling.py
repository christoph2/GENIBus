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
import logging
from genicontrol.units import UnitTable

logger = logging.getLogger("GeniControl")

InfoTuple = namedtuple('InfoTuple', 'header unit range zero')
ScalingTuple = namedtuple('ScalingTuple', 'physEntity factor unit valueInterpretation byteOrder scaleInformationFormat signOfZero')

class MalformedScalingInformationError(Exception): pass

def getScalingInfo(infoTuple):
    header = infoTuple.head
    unit = infoTuple.unit
    if (header & 0xc0) != 0x80:
        raise MalformedScalingInformationError()
    else:
        valueInterpretation = (header & 0x20) >> 5
        byteOrder = (header & 0x10) >> 6
        scaleInformationFormat = (header & 0x03)
        if unit:
             signOfZero = (unit & 0x80) >> 7
             unit &= 0x7f
             ut = UnitTable[unit]
             factor = ut.factor
             physEntity = ut.physEntity
             unt = ut.unit
        else:
             factor = '-'
             physEntity = '-'
             unt = '-'
             signOfZero = '-'

        return ScalingTuple(physEntity, factor, unt, valueInterpretation, byteOrder, scaleInformationFormat, signOfZero)


