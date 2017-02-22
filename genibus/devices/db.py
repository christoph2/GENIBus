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

from collections import namedtuple
import glob
import json
import os
import pkgutil
from pprint import pprint
import sqlite3
import sys
import genibus.devices
from genibus.utils.classes import SingletonBase

DataitemByClass = namedtuple('DataitemByClass', 'name, id, access, note')
DataitemByClassAndName = namedtuple('DataitemByClassAndName', 'id, klass, access, note')

class DeviceDB(SingletonBase):

    def __init__(self):
        self.open()
        self.importFiles()

    def createSchema(self):
        #print("Creating schema...")
        self.cursor.execute("""
            CREATE TABLE dataitems(
                model CHAR(64) NOT NULL, name CHAR(64) NOT NULL,
                class INT NOT NULL, id INT NOT NULL, access INT NOT NULL, note CHAR(64) DEFAULT NULL,
                PRIMARY KEY(model, name)
            );
        """)

        self.cursor.execute("""CREATE TABLE units(
            id INT NOT NULL PRIMARY KEY,physicalEntity CHAR(64), prefix DOUBLE, Unit CHAR(8)
            );
        """)
        self.conn.commit()

    def open(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.createSchema()

    def toList(self, *args):
        result = []
        for elem in args:
            if isinstance(elem, (list, tuple)):
                result.extend(list(elem))
            else:
                result.append(elem)
        return result

    def importFiles(self):
        _dir = os.path.dirname(sys.modules['genibus.devices'].__file__)
        for dp in glob.glob("{0}{1}*.json".format(_dir, os.sep)):
            _, fullname = os.path.split(dp)
            model = fullname.split('.')[0]
            with open(dp) as filePointer:
                data = json.load(filePointer)
            for row  in data:
                self.conn.execute("INSERT INTO dataitems VALUES(?, ?, ?, ?, ?, ?)", self.toList(model, row))
        self.conn.commit()
        data = pkgutil.get_data('genibus.config', 'units.json')
        units = json.loads(data.decode('latin-1'), encoding = 'utf-8')
        for key, unit in units.items():
            unit[0] = unit[0].strip()
            self.conn.execute("INSERT INTO units VALUES(?, ?, ?, ?)", self.toList(key, unit))
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def dataitems(self, model):
        self.cursor.execute("SELECT * FROM dataitems WHERE model = ? ORDER BY class, id;", (model, ))
        result = self.cursor.fetchall()
        return result

    def dataitemsByClass(self, model, klass):
        self.cursor.execute("SELECT name, id, access, note FROM dataitems WHERE model = ? AND class = ? ORDER BY id;", (model, klass))
        result = self.cursor.fetchall()
        if result:
            return {d.name: d for d in [DataitemByClass(*x) for x in result] }
        return result

    def dataitemByClassAndName(self, model, name):
        self.cursor.execute("SELECT id, class, access, note FROM dataitems WHERE model = ? AND name = ?;", (model, name))
        result = self.cursor.fetchall()
        return DataitemByClassAndName(*result[0]) if result else []

    def units(self):
        self.cursor.execute("SELECT * FROM units ORDER BY id;")
        result = self.cursor.fetchall()
        return result

    def unitEnities(self):
        self.cursor.execute("SELECT DISTINCT(physicalEntity) FROM units ORDER BY 1;")
        result = self.cursor.fetchall()
        return result

    def unitsByEntity(self, entity):
        self.cursor.execute("SELECT * FROM units WHERE physicalEntity = ? ORDER BY id;", (entity, ))
        result = self.cursor.fetchall()
        return result

