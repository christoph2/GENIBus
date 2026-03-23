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
__author__ = "Christoph Schueler"
__version__ = "0.1.0"

import logging
from typing import Optional, Tuple, Union


class Logger(object):

    LOGGER_BASE_NAME = "genibus"
    FORMAT = "[%(levelname)s (%(name)s)]: %(message)s"

    def __init__(self, level: int = logging.WARN) -> None:
        self.logger = logging.getLogger("{0}".format(self.LOGGER_BASE_NAME))
        self.logger.setLevel(level)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(level)
            formatter = logging.Formatter(self.FORMAT)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.lastMessage: Optional[str] = None
        self.lastSeverity: Optional[int] = None

    def get_last_error(self) -> Tuple[Optional[int], Optional[str]]:
        result = (self.lastSeverity, self.lastMessage)
        self.lastSeverity = None
        self.lastMessage = None
        return result

    def getLastError(self) -> Tuple[Optional[int], Optional[str]]:
        return self.get_last_error()

    def log(self, message: str, level: int) -> None:
        self.lastSeverity = level
        self.lastMessage = message
        self.logger.log(level, "{0}".format(message))

    def info(self, message: str) -> None:
        self.log(message, logging.INFO)

    def warn(self, message: str) -> None:
        self.log(message, logging.WARN)

    def error(self, message: str) -> None:
        self.log(message, logging.ERROR)

    def debug(self, message: str) -> None:
        self.log(message, logging.DEBUG)

    def critical(self, message: str) -> None:
        self.log(message, logging.CRITICAL)

    def verbose(self) -> None:
        self.logger.setLevel(logging.DEBUG)

    def silent(self) -> None:
        self.logger.setLevel(logging.CRITICAL)

    def set_level(self, level: Union[str, int]) -> None:
        level_map = {
            "INFO": logging.INFO,
            "WARN": logging.WARN,
            "DEBUG": logging.DEBUG,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        normalized = level
        if isinstance(level, str):
            normalized = level_map.get(level.upper(), logging.WARN)
        self.logger.setLevel(int(normalized))

    def setLevel(self, level: Union[str, int]) -> None:
        self.set_level(level)
