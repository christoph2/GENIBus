#!/usr/bin/env python
"""Allgemeine Klassen-Hilfen fuer Singleton- und Repr-Patterne."""

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
__author__ = "Christoph Schueler"
__version__ = "0.1.0"


import threading
from typing import Any

from genibus.utils import helper


class SingletonBase:
    """Thread-sichere Singleton-Basisklasse per Double-Checked-Locking."""

    _lock = threading.Lock()

    def __new__(cls, *args: Any, **kws: Any) -> Any:
        """Erzeugt genau eine Instanz pro abgeleiteter Klasse.

        Args:
            *args: Positionale Konstruktionsargumente.
            **kws: Benannte Konstruktionsargumente.

        Returns:
            Any: Singleton-Instanz der abgeleiteten Klasse.
        """
        # Double-Checked Locking
        if not hasattr(cls, "_instance"):
            try:
                cls._lock.acquire()
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
            finally:
                cls._lock.release()
        return cls._instance


class RepresentationMixIn:
    """Mix-in fuer konsistente, mehrzeilige Debug-`repr()`-Ausgabe."""

    def _repr_lines(self) -> list[str]:
        """Erzeugt die einzelnen Zeilen der Textrepräsentation.

        Returns:
            list[str]: Zeilenweise Repräsentation inklusive Header/Footer.
        """
        keys = [k for k in self.__dict__ if not (k.startswith("__") and k.endswith("__"))]
        result = []
        result.append(f"{self.__class__.__name__} {{")
        for key in keys:
            value = getattr(self, key)
            if isinstance(value, int):
                line = f"    {key} = 0x{value:X}"
            elif isinstance(value, (float, type(None))):
                line = f"    {key} = {value}"
            elif isinstance(value, bytearray):
                line = f"    {key} = {helper.hex_dump(value)}"
            else:
                line = f"    {key} = '{value}'"
            result.append(line)
        result.append("}")
        return result

    def __repr__(self) -> str:
        """Liefert eine lesbare, mehrzeilige Repräsentation des Objekts."""
        return "\n".join(self._repr_lines())
