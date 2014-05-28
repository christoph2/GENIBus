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

import locale
import logging
logger = logging.getLogger("GeniControl")

from decimal import Decimal as D

locale.setlocale(locale.LC_ALL, '')

def asLocaleString(value):
    return locale.format("%0.2f", value, True)

def convertForward8(x, zero, range, unit):
    return (D(zero) + (D(x & 0xff) * (D(range) / D('254.0')))) * D(unit)


def convertReverse8(x, zero, range, unit):
    return (D('254.0') / (D(range) * D(unit))) * ((D(-zero) * D(unit)) + D(x))


def convertForward16(x, zero, range, unit):
    return (D(zero) + (D(x & 0xffff) * (D(range) / (D('254.0') * D('256.0'))))) * D(unit)


def convertReverse16(x, zero, range, unit):
    return ((D('254.0') * D('256.0'))/ (D(range) * D(unit))) * ((D(-zero) * D(unit)) + D(x))


