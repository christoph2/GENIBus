#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.1.0"

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


import logging
import threading
from genibus.linklayer.connection import ConnectionIF

logger = logging.getLogger("GeniControl")

try:
    import serial
except ImportError:
    logger.debug("pySerial not installed.")
    serialAvailable = False
else:
    serialAvailable = True

class SerialPort(ConnectionIF):
    DRIVER = 'Serial port'
    _lock = threading.Lock()
    counter = 0

    def __init__(self, portName, baudrate = 9600, bytesize = serial.EIGHTBITS,
                 parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, timeout = 0.5):
        super(SerialPort, self).__init__()
        self._portName = portName
        self._port = None
        self._baudrate = baudrate
        self._bytesize = bytesize
        self._parity = parity
        self._stopbits = stopbits
        self._timeout = timeout
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
            raise
        self._logger.info("Serial port openend as '%s' @ %d Bits/Sec.", self._port.portstr, self._port.baudrate)
        self.connected = True
        return True

    def write(self, data):
        self.output(True)
        self._port.write(bytearray(list(data)))
        self.flush()

    def read(self):
        self.output(False)
        result = bytearray(self._port.read(self._port.in_waiting))
        return result

    def output(self, enable):
        if enable:
            self._port.rts = False
            self._port.dtr = False
        else:
            self._port.rts = True
            self._port.dtr = True

    def flush(self):
        self._port.flush()

    def disconnect(self):
        if self._port.isOpen() == True:
            self._port.close()

    close = disconnect


