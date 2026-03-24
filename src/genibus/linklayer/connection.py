#!/usr/bin/env python
"""Abstrakte Schnittstelle fuer GENIBus-Transporte.

Dieses Modul definiert das gemeinsame Interface fuer synchrone Transporttreiber
wie TCP und Serial. Implementierungen muessen den Lebenszyklus (`connect`,
`disconnect`, `close`) sowie den I/O-Pfad (`write`, `read`) bereitstellen.
"""

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
from abc import ABC, abstractmethod
from collections.abc import Iterable
from types import TracebackType
from typing import ClassVar


class ConnectionIF(ABC):
    """Basisklasse fuer alle Linklayer-Transporte.
    """

    DRIVER: ClassVar[str] = "Unknown"

    def __init__(self) -> None:
        self._logger = logging.getLogger("GeniControl:" + self.DRIVER)

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            # Destructors must not raise.
            pass

    def __enter__(self) -> "ConnectionIF":
        """Oeffnet die Verbindung fuer den Context-Manager.

        Returns:
            ConnectionIF: Die geoeffnete Instanz.
        """
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Schliesst die Verbindung beim Verlassen des Context-Managers."""
        self.close()

    @abstractmethod
    def connect(self) -> bool:
        """Stellt die physische oder logische Verbindung her.

        Returns:
            bool: `True`, wenn die Verbindung erfolgreich hergestellt wurde.
        """
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> None:
        """Trennt eine bestehende Verbindung."""
        raise NotImplementedError

    @abstractmethod
    def write(self, data: Iterable[int]) -> None:
        """Sendet Bytedaten ueber den Treiber.

        Args:
            data: Iterierbare Ganzzahlen im Bereich 0..255.
        """
        raise NotImplementedError

    @abstractmethod
    def read(self) -> bytearray | None:
        """Liest empfangene Bytedaten aus dem Treiber.

        Returns:
            bytearray | None: Empfangene Daten oder `None`, wenn nichts
            verfuegbar ist.
        """
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """Schliesst alle vom Treiber belegten Ressourcen."""
        raise NotImplementedError

    def get_driver(self) -> str:
        """Gibt den Treibernamen zurueck."""
        return self.DRIVER

    def getDriver(self) -> str:
        """Legacy-Alias fuer `get_driver()`."""
        return self.get_driver()

    @property
    def display_name(self) -> str:
        """Anzeigename des Treibers fuer UI-Zwecke."""
        return self.DRIVER

    @property
    def displayName(self) -> str:
        """Legacy-Alias fuer `display_name`."""
        return self.display_name
