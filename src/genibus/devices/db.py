#!/usr/bin/env python
"""In-Memory-Datenbank fuer GENIBus-Datapoints und Einheiten.

Dieses Modul laedt JSON-Modelldaten aus Paketressourcen und stellt
Lookup-Methoden fuer Datapoints und physikalische Einheiten bereit.
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

import json
import sqlite3
from collections import namedtuple
from collections.abc import Sequence
from importlib import resources
from pathlib import Path
from typing import Any

from genibus.utils.classes import SingletonBase

DataitemByClass = namedtuple("DataitemByClass", "name, id, access, note")
DataitemByClassAndName = namedtuple("DataitemByClassAndName", "id, klass, access, note")


class DeviceDB(SingletonBase):
    """Singleton-Datenbank fuer Geraetemodelle und Einheiten."""

    def __init__(self) -> None:
        """Initialisiert die In-Memory-DB und importiert Ressourcen."""
        self.open()
        self.import_files()

    def create_schema(self) -> None:
        """Erzeugt die Tabellen `dataitems` und `units`."""
        self.cursor.execute(
            """
            CREATE TABLE dataitems(
                model CHAR(64) NOT NULL, name CHAR(64) NOT NULL,
                class INT NOT NULL, id INT NOT NULL, access INT NOT NULL,
                note CHAR(64) DEFAULT NULL,
                PRIMARY KEY(model, name)
            );
        """
        )

        self.cursor.execute(
            """CREATE TABLE units(
            id INT NOT NULL PRIMARY KEY,physicalEntity CHAR(64), prefix DOUBLE, Unit CHAR(8)
            );
        """
        )
        self.conn.commit()

    def open(self) -> None:
        """Oeffnet die SQLite-In-Memory-Datenbank und erstellt das Schema."""
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.create_schema()

    def to_list(self, *args: Any) -> list[Any]:
        """Flacht gemischte Argumente zu einer flachen Liste ab.

        Args:
            *args: Einzelwerte oder Sequenzen.

        Returns:
            list[Any]: Flache Liste aller Werte.
        """
        result: list[Any] = []
        for elem in args:
            if isinstance(elem, (list, tuple)):
                result.extend(list(elem))
            else:
                result.append(elem)
        return result

    def import_files(self) -> None:
        """Importiert Modell-JSONs und `units.json` in die DB."""
        devices_root = resources.files("genibus.devices")
        for datapoint_file in devices_root.iterdir():
            file_name = Path(datapoint_file.name)
            if file_name.suffix.lower() != ".json":
                continue

            model = file_name.stem
            with datapoint_file.open(encoding="utf-8") as filePointer:
                data = json.load(filePointer)

            for row in data:
                self.conn.execute(
                    "INSERT INTO dataitems VALUES(?, ?, ?, ?, ?, ?)",
                    self.to_list(model, row),
                )
        self.conn.commit()

        units_json = (
            resources.files("genibus.config")
            .joinpath("units.json")
            .read_text(encoding="latin-1")
        )
        units = json.loads(units_json)
        for key, unit in units.items():
            unit[0] = unit[0].strip()
            self.conn.execute("INSERT INTO units VALUES(?, ?, ?, ?)", self.to_list(int(key), unit))
        self.conn.commit()

    def close(self) -> None:
        """Schreibt ausstehende Aenderungen und schliesst DB-Ressourcen."""
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def data_items(self, model: str) -> list[Sequence[Any]]:
        """Liefert alle Datapoints eines Modells.

        Args:
            model: Modellname, z. B. ``magna``.

        Returns:
            list[Sequence[Any]]: SQL-Resultset sortiert nach Klasse und ID.
        """
        self.cursor.execute("SELECT * FROM dataitems WHERE model = ? ORDER BY class, id;", (model,))
        result = self.cursor.fetchall()
        return result

    def data_items_by_class(self, model: str, klass: int) -> Any:
        """Liefert Datapoints eines Modells gefiltert nach APDU-Klasse.

        Args:
            model: Modellname.
            klass: APDU-Klassen-ID.

        Returns:
            Any: Dict ``name -> DataitemByClass`` oder leere Liste.
        """
        self.cursor.execute(
            "SELECT name, id, access, note FROM dataitems "
            "WHERE model = ? AND class = ? ORDER BY id;",
            (model, klass),
        )
        result = self.cursor.fetchall()
        if result:
            return {d.name: d for d in [DataitemByClass(*x) for x in result]}
        return result

    def data_item_by_class_and_name(self, model: str, name: str) -> Any:
        """Liefert einen Datapoint per Modell und Name.

        Args:
            model: Modellname.
            name: Datapoint-Name.

        Returns:
            Any: `DataitemByClassAndName` oder leere Liste.
        """
        self.cursor.execute(
            "SELECT id, class, access, note FROM dataitems WHERE model = ? AND name = ?;",
            (model, name),
        )
        result = self.cursor.fetchall()
        return DataitemByClassAndName(*result[0]) if result else []

    def units(self) -> list[Sequence[Any]]:
        """Liefert alle Einheiten aus der `units`-Tabelle."""
        self.cursor.execute("SELECT * FROM units ORDER BY id;")
        result = self.cursor.fetchall()
        return result

    def unit_entities(self) -> list[Sequence[Any]]:
        """Liefert alle unterschiedlichen physikalischen Einheitsklassen."""
        self.cursor.execute("SELECT DISTINCT(physicalEntity) FROM units ORDER BY 1;")
        result = self.cursor.fetchall()
        return result

    def units_by_entity(self, entity: str) -> list[Sequence[Any]]:
        """Liefert alle Einheiten fuer eine physikalische Klasse.

        Args:
            entity: Name der physikalischen Klasse, z. B. ``Voltage``.

        Returns:
            list[Sequence[Any]]: Zugehoerige Einheitseintraege.
        """
        self.cursor.execute("SELECT * FROM units WHERE physicalEntity = ? ORDER BY id;", (entity,))
        result = self.cursor.fetchall()
        return result

    # Backward-compatible camelCase aliases.
    def createSchema(self) -> None:
        """Legacy-Alias fuer `create_schema()`."""
        return self.create_schema()

    def toList(self, *args: Any) -> list[Any]:
        """Legacy-Alias fuer `to_list()`."""
        return self.to_list(*args)

    def importFiles(self) -> None:
        """Legacy-Alias fuer `import_files()`."""
        return self.import_files()

    def dataitems(self, model: str) -> list[Sequence[Any]]:
        """Legacy-Alias fuer `data_items()`."""
        return self.data_items(model)

    def dataitemsByClass(self, model: str, klass: int) -> Any:
        """Legacy-Alias fuer `data_items_by_class()`."""
        return self.data_items_by_class(model, klass)

    def dataitemByClassAndName(self, model: str, name: str) -> Any:
        """Legacy-Alias fuer `data_item_by_class_and_name()`."""
        return self.data_item_by_class_and_name(model, name)

    def unitEnities(self) -> list[Sequence[Any]]:
        """Legacy-Alias fuer `unit_entities()`."""
        return self.unit_entities()

    def unitsByEntity(self, entity: str) -> list[Sequence[Any]]:
        """Legacy-Alias fuer `units_by_entity()`."""
        return self.units_by_entity(entity)

