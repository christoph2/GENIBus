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


import array
import logging
import os
from genicontrol.defs import CONFIGURATION_DIRECTORY

logger = logging.getLogger("genicontrol")

def makeWord(bh, bl):
    return (bh <<8) | bl

def hiByte(w):
    return (w & 0xff00) >> 8

def loByte(w):
    return w & 0x00ff

def bytes(w):
    return tuple(hiByte(w), loByte(w))

def makeBuffer(arr):
    return buffer(array.array('B', arr))

def makeArray(buf):
    return tuple([ord(x) for x in str(buf)])

def absConfigurationFilename(fname):
    return os.path.join(CONFIGURATION_DIRECTORY, fname)

