#!/usr/bin/env python

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
from collections.abc import Iterable

from genibus.linklayer.connection import ConnectionIF

logger = logging.getLogger("GeniControl")

try:
    import serial  # type: ignore[import-untyped]
except ImportError:
    logger.debug("pySerial not installed.")
    serial = None
    serial_available = False
else:
    serial_available = True

if serial_available:
    _BYTESIZE_DEFAULT = serial.EIGHTBITS
    _PARITY_DEFAULT = serial.PARITY_NONE
    _STOPBITS_DEFAULT = serial.STOPBITS_ONE
else:
    _BYTESIZE_DEFAULT = 8
    _PARITY_DEFAULT = "N"
    _STOPBITS_DEFAULT = 1


class SerialPort(ConnectionIF):
    DRIVER = "Serial port"
    _lock = threading.Lock()
    counter = 0

    def __init__(
        self,
        portName: str,
        baudrate: int = 9600,
        bytesize: int = _BYTESIZE_DEFAULT,
        parity: str = _PARITY_DEFAULT,
        stopbits: int = _STOPBITS_DEFAULT,
        timeout: float = 0.5,
    ) -> None:
        super().__init__()
        self._portName = portName
        self._port = None
        self._baudrate = baudrate
        self._bytesize = bytesize
        self._parity = parity
        self._stopbits = stopbits
        self._timeout = timeout
        self.connected = False

    def connect(self) -> bool:
        if not serial_available:
            raise RuntimeError("pySerial not installed.")

        SerialPort.counter += 1
        self._logger.debug("Trying to open serial port %s.", self._portName)
        try:
            self._port = serial.Serial(
                self._portName,
                self._baudrate,
                self._bytesize,
                self._parity,
                self._stopbits,
                self._timeout,
            )
        except serial.SerialException as exc:
            self._logger.error("%s", exc)
            raise

        assert self._port is not None

        self._logger.info(
            "Serial port openend as '%s' @ %d Bits/Sec.",
            self._port.portstr,
            self._port.baudrate,
        )
        self.connected = True
        return True

    def write(self, data: Iterable[int]) -> None:
        if not self.connected or self._port is None:
            raise RuntimeError("Serial port is not connected.")

        self.set_output(True)
        self._port.write(bytearray(list(data)))
        self.flush_output()

    def read(self) -> bytearray:
        if not self.connected or self._port is None:
            raise RuntimeError("Serial port is not connected.")

        self.set_output(False)
        in_waiting = getattr(self._port, "in_waiting", 0)
        result = bytearray(self._port.read(in_waiting))
        return result

    def set_output(self, enable: bool) -> None:
        if self._port is None:
            raise RuntimeError("Serial port is not connected.")

        if enable:
            self._port.rts = False
            self._port.dtr = False
        else:
            self._port.rts = True
            self._port.dtr = True

    def output(self, enable: bool) -> None:
        self.set_output(bool(enable))

    def flush_output(self) -> None:
        if self._port is None:
            raise RuntimeError("Serial port is not connected.")
        self._port.flush()

    def flush(self) -> None:
        self.flush_output()

    def disconnect(self) -> None:
        if self.connected and self._port is not None:
            self._port.close()
        self.connected = False

    close = disconnect


