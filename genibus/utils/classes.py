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
__author__  = 'Christoph Schueler'
__version__ = '0.1.0'


import threading
import types
from genibus.utils import helper


class SingletonBase(object):
    _lock = threading.Lock()

    def __new__(cls, *args, **kws):
        # Double-Checked Locking
        if not hasattr(cls, '_instance'):
            try:
                cls._lock.acquire()
                if not hasattr(cls, '_instance'):
                    cls._instance = super(SingletonBase, cls).__new__(cls)
            finally:
                cls._lock.release()
        return cls._instance


class RepresentationMixIn(object):

    def __repr__(self):
        keys = [k for k in self.__dict__ if not (k.startswith('__') and k.endswith('__'))]
        result = []
        result.append("%s {" % self.__class__.__name__)
        for key in keys:
            value = getattr(self, key)
            if isinstance(value, (int, long)):
                line = "    %s = 0x%X" % (key, value)
            elif isinstance(value, (float, types.NoneType)):
                line = "    %s = %s" % (key, value)
            elif isinstance(value, bytearray):
                line = "    %s = %s" % (key, helper.hexDump(value))
            else:
                line = "    %s = '%s'" % (key, value)
            result.append(line)
        result.append("}")
        return '\n'.join(result)

