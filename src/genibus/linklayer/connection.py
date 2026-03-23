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


from abc import ABC, abstractmethod
import logging
from typing import ClassVar, Iterable, Optional


class ConnectionIF(ABC):
    DRIVER: ClassVar[str] = "Unknown"

    def __init__(self) -> None:
        self._logger = logging.getLogger("GeniControl:" + self.DRIVER)

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            # Destructors must not raise.
            pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    @abstractmethod
    def connect(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def write(self, data: Iterable[int]) -> None:
        raise NotImplementedError

    @abstractmethod
    def read(self) -> Optional[bytearray]:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    def get_driver(self) -> str:
        return self.DRIVER

    def getDriver(self) -> str:
        return self.get_driver()

    @property
    def display_name(self) -> str:
        return self.DRIVER

    @property
    def displayName(self) -> str:
        return self.display_name
