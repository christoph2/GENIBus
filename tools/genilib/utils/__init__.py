#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2016 by Christoph Schueler <github.com/Christoph2,
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
import sys
from genicontrol.defs import CONFIGURATION_DIRECTORY

logger = logging.getLogger("GeniControl")

def makeWord(bh, bl):
    return (bh <<8) | bl

def hiByte(w):
    return (w & 0xff00) >> 8

def loByte(w):
    return w & 0x00ff

def bytes(w):
    return tuple((hiByte(w), loByte(w)))

def makeBuffer(arr):
    return buffer(array.array('B', arr))

def makeArray(buf):
    return tuple([ord(x) for x in str(buf)])

def absConfigurationFilename(fname):
    return os.path.join(CONFIGURATION_DIRECTORY, fname)

def dumpHex(arr):
    return [hex(x) for x in arr]


if sys.version_info.major == 3:
    from io import BytesIO as StringIO
else:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO


def createStringBuffer(*args):
    """Create a string with file-like behaviour (StringIO on Python 2.x).
    """
    return StringIO(*args)

def binExtractor(fname, offset, length):
    """Extract a junk of data from a file.
    """
    fp = open(fname)
    fp.seek(offset)
    data = fp.read(length)
    return data

CYG_PREFIX = "/cygdrive/"

def cygpathToWin(path):
    if path.startswith(CYG_PREFIX):
        path = path[len(CYG_PREFIX) : ]
        driveLetter = "{0}:\\".format(path[0])
        path = path[2 : ].replace("/", "\\")
        path = "{0}{1}".format(driveLetter, path)
    return path


import ctypes

class StructureWithEnums(ctypes.Structure):
    """Add missing enum feature to ctypes Structures.
    """
    _map = {}

    def __getattribute__(self, name):
        _map = ctypes.Structure.__getattribute__(self, '_map')
        value = ctypes.Structure.__getattribute__(self, name)
        if name in _map:
            EnumClass = _map[name]
            if isinstance(value, ctypes.Array):
                return [EnumClass(x) for x in value]
            else:
                return EnumClass(value)
        else:
            return value

    def __str__(self):
        result = []
        result.append("struct {0} {{".format(self.__class__.__name__))
        for field in self._fields_:
            attr, attrType = field
            if attr in self._map:
                attrType = self._map[attr]
            value = getattr(self, attr)
            result.append("    {0} [{1}] = {2!r};".format(attr, attrType.__name__, value))
        result.append("};")
        return '\n'.join(result)

    __repr__ = __str__


import subprocess

class CommandError(Exception):
    pass

def runCommand(cmd):
    proc = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    result = proc.communicate()
    proc.wait()
    if proc.returncode:
        raise CommandError("{0}".format(result[1]))
    return result[0]
