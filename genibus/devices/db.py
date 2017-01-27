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

import glob
import json
import os
import pkgutil
from pprint import pprint
import sqlite3
import sys
import genibus.devices
from genibus.utils.classes import SingletonBase

class DeviceDB(SingletonBase):

    def __init__(self):
        self.open()
        self.importDevices()

    def createSchema(self):
        print("Creating schema...")

        self.cursor.execute("""
            CREATE TABLE dataitems(
                model CHAR(64) NOT NULL, name CHAR(64) NOT NULL,
                class INT NOT NULL, id INT NOT NULL, access INT NOT NULL, note CHAR(64) DEFAULT NULL,
                PRIMARY KEY(model, name)
            );""")
        self.conn.commit()

    def open(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.createSchema()

    def importDevices(self):
        for dp in glob.glob("{0}{1}*.json".format(os.path.dirname(sys.modules['genibus.devices'].__file__), os.sep)):
            _, fullname = os.path.split(dp)
            model = fullname.split('.')[0]
            data = json.load(open(dp))
            for row  in data:
                self.conn.execute("INSERT INTO dataitems VALUES(?, ?, ?, ?, ?, ?)", (model, *row))
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def select(self, table):
        self.cursor.execute("SELECT * FROM {0};".format(table))
        result = self.cursor.fetchall();
        return result

#db = DeviceDB()
#pprint(db.select("dataitems"))
#db.close()

