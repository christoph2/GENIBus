#!/usr/bin/env python

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

import ctypes
import subprocess
from collections.abc import Callable, Sequence
from typing import Any, TypeVar, cast

T = TypeVar("T")


def slicer(
    iterable: Sequence[T],
    sliceLength: int,
    converter: Callable[[Sequence[T]], Any] | None = None,
) -> list[Any]:
    converter_fn: Callable[[Sequence[T]], Any]
    if converter is None:
        converter_fn = cast(Callable[[Sequence[T]], Any], type(iterable))
    else:
        converter_fn = converter

    length = len(iterable)
    return [
        converter_fn(iterable[item : item + sliceLength])
        for item in range(0, length, sliceLength)
    ]


CYG_PREFIX = "/cygdrive/"


def cygpathToWin(path: str) -> str:
    return cygpath_to_win(path)


def cygpath_to_win(path: str) -> str:
    if path.startswith(CYG_PREFIX):
        path = path[len(CYG_PREFIX) :]
        drive_letter = f"{path[0]}:\\"
        path = path[2:].replace("/", "\\")
        path = f"{drive_letter}{path}"
    return path


class StructureWithEnums(ctypes.Structure):
    """Add missing enum feature to ctypes Structures."""

    _map: dict[str, Any] = {}

    def __getattribute__(self, name: str) -> Any:
        enum_map = ctypes.Structure.__getattribute__(self, "_map")
        value = ctypes.Structure.__getattribute__(self, name)
        if name in enum_map:
            enum_class = enum_map[name]
            if isinstance(value, ctypes.Array):
                return [enum_class(x) for x in value]
            return enum_class(value)
        return value

    def __str__(self) -> str:
        result = [f"struct {self.__class__.__name__} {{"]
        for field in self._fields_:
            attr = field[0]
            attr_type = field[1]
            if attr in self._map:
                attr_type = self._map[attr]
            value = getattr(self, attr)
            result.append(f"    {attr} [{attr_type.__name__}] = {value!r};")
        result.append("};")
        return "\n".join(result)

    __repr__ = __str__


class CommandError(Exception):
    pass


def runCommand(cmd: str) -> bytes:
    return run_command(cmd)


def run_command(cmd: str) -> bytes:
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    result = proc.communicate()
    proc.wait()
    if proc.returncode:
        stderr_output = result[1].decode("utf-8", errors="replace")
        raise CommandError(stderr_output)
    return result[0]

