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
import threading
from genicontrol.connection import ConnectionIF

logger = logging.getLogger("GeniControl")

try:
    import serial
except ImportError:
    logger.debug("pySerial not installed.")
    serialAvailable = False
else:
    serialAvailable = True

class SerialPort(ConnectionIF):
    _lock = threading.Lock()
    _logger = logger
    counter = 0

    def __init__(self, portName, baudrate = 9600, bytesize = 8,
                 parity = 'N', stopbits = 1, timeout = 0.5):
        self._portName = portName
        self._port = None
        self._baudrate = baudrate
        self._bytesize = bytesize
        self._parity = parity
        self._stopbits = stopbits
        self._timeout = timeout
        self._rtsSupported = True
        self._lastWritten = None
        self.connected = False

    def connect(self):
        SerialPort.counter += 1
        self._logger.debug("Trying to open serial port %s.", self._portName)
        try:
            self._port = serial.Serial(self._portName, self._baudrate , self._bytesize, self._parity,
                self._stopbits, self._timeout
            )
        except serial.SerialException as e:
            self._logger.error("%s", e)
            print("Cannot open serial port '%s': %s" % (self._portName, e))
            return False
        self._logger.info("Serial port openend as '%s' @ %d Bits/Sec.", self._port.portstr, self._port.baudrate)
        self.connected = True
        return True

    def write(self, data):
        data = bytearray(list(data))
        self._port.reset_input_buffer()     # Drop stale / unsolicited bytes.
        self.output(True)
        self._port.write(data)
        self.flush()
        self._lastWritten = bytes(data)

    def _readFrame(self):
        """Read one GENIbus frame: SD, LEN, DA, SA, APDUs..., CRC_H, CRC_L (LEN + 4 bytes)."""
        head = self._port.read(2)
        if len(head) < 2:
            return bytes(head)
        rest = self._port.read(head[1] + 2)
        return bytes(head) + bytes(rest)

    def read(self, length = 0x100):
        self.output(False)
        data = self._readFrame()
        if data and self._lastWritten and data == self._lastWritten:
            # Some RS485 adapters echo the transmitted telegram -- skip it.
            data = self._readFrame()
        self._lastWritten = None
        if not data:
            return None
        return array.array('B', bytearray(data))

    def output(self, enable):
        # RS485 direction control via RTS/DTR (for adapters without automatic direction control).
        # Not every adapter / driver supports this, so failures are ignored.
        if not self._rtsSupported:
            return
        try:
            if enable:
                self._port.rts = False
                self._port.dtr = False
            else:
                self._port.rts = True
                self._port.dtr = True
        except (IOError, OSError, ValueError) as e:
            self._logger.info("RTS/DTR control not supported by '%s' (%s), ignored.", self._portName, e)
            self._rtsSupported = False

    def flush(self):
        self._port.flush()

    def disconnect(self):
        self.connected = False
        if self._port is not None and self._port.is_open:
            self._port.close()

    close = disconnect

    @property
    def displayName(self):
        return "Serial port %s" % self._portName


