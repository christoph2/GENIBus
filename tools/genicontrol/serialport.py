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
import threading

try:
    import serial
except ImportError:
    print "pySerial not installed."
    serialAvailable = False
else:
    serialAvailable = True

class SerialPort(object):
    _lock = threading.Lock()
    _logger = logging.getLogger("genicontrol")

##
##    def __new__(cls):
##        try:
##            cls._lock.acquire()
##            if not hasattr(cls, '_instance'):
##                cls._instance = super(cls.__class__, cls).__new__(cls)
##        finally:
##            cls._lock.release()
##        return cls._instance
##

    def __init__(self, portNum, baudrate = 19200, bytesize = serial.EIGHTBITS,
                 parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, timeout = 0.1):
        self._portNum = portNum
        self._baudrate = baudrate
        self._bytesize = bytesize
        self._parity = parity
        self._stopbits = stopbits
        self._timeout = timeout

    def open(self):
        self._logger.debug("Trying to open serial port #%u.", self._portNum)
        try:
            self._port = serial.Serial(self._portNum, self._baudrate , self._bytesize, self._parity,
                self._stopbits, self._timeout
            )
        except serial.SerialException as e:
            self._logger.error("%s", e)
            #self._logger.exception(e)
            raise
        self._logger.info("Serial port openend as '%s' @ %d Bits/Sec.", self._port.portstr, self._port.baudrate)

    def write(self, data):
        #print list(data)
        self._port.write(bytearray(list(data)))

    def read(self, length):
        result = self._port.read(length)
        print result
        return result

    def close(self):
        if self._port.isOpen() == True:
            self._port.close()

    @property
    def displayName(self):
        return "Serial port"


