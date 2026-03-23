#!/usr/bin/env python

__version__ = "0.1.0"

__copyright__ = """
Grundfos GENIBus Library for Arduino.

(C) 2007-2014 by Christoph Schueler <github.com/Christoph2,
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
import socket
from collections.abc import Iterable

from genibus.linklayer.connection import ConnectionIF

logger = logging.getLogger("GeniControl")

BUF_SIZE = 1024

socket.setdefaulttimeout(0.5)


class Connector(ConnectionIF):
    DRIVER = "TCP"

    def __init__(
        self,
        server_ip: str | None = None,
        server_port: int | None = None,
        serverIP: str | None = None,
        serverPort: int | None = None,
        timeout: float = 0.5,
        buffer_size: int = BUF_SIZE,
    ) -> None:
        super().__init__()
        self.server_ip = server_ip if server_ip is not None else serverIP
        self.server_port = server_port if server_port is not None else serverPort
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.sock: socket.socket | None = None
        self.connected = False

        # Legacy attribute aliases.
        self.serverIP = self.server_ip
        self.serverPort = self.server_port

    def connect(self) -> bool:
        if self.server_ip is None or self.server_port is None:
            raise ValueError("server_ip and server_port must be set before connect().")

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.settimeout(self.timeout)
            self.sock.connect((self.server_ip, int(self.server_port)))
            self.connected = True
            return True
        except Exception as exc:
            self._logger.error("TCP connect failed: %s", exc)
            self.connected = False
            return False

    def disconnect(self) -> None:
        if self.sock is not None:
            self.sock.close()
        self.sock = None
        self.connected = False

    def close(self) -> None:
        self.disconnect()

    def write(self, data: Iterable[int]) -> None:
        if not self.connected or self.sock is None:
            raise RuntimeError("TCP connector is not connected.")
        self.sock.sendall(bytearray(data))

    def read(self) -> bytearray | None:
        if not self.connected or self.sock is None:
            return None
        data = bytearray(self.sock.recv(self.buffer_size))
        return data


def connection_factory(driver: str) -> str:
    if driver == "0":
        return "Simulator"
    return "Arduino / TCP"


def ConnectionFactory(driver: str) -> str:
    return connection_factory(driver)
