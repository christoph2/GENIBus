from genibus.devices.db import DeviceDB


def test_data_items_by_class_and_alias_match() -> None:
    db = DeviceDB()

    modern = db.data_items_by_class("magna", 2)
    legacy = db.dataitemsByClass("magna", 2)

    assert modern == legacy
    assert "p" in modern


def test_data_item_by_class_and_name_and_alias_match() -> None:
    db = DeviceDB()

    modern = db.data_item_by_class_and_name("magna", "ref_loc")
    legacy = db.dataitemByClassAndName("magna", "ref_loc")

    assert modern == legacy
    assert modern.id == 40


def test_unit_entities_and_alias_match() -> None:
    db = DeviceDB()

    modern = db.unit_entities()
    legacy = db.unitEnities()

    assert modern == legacy
    assert ("Voltage",) in modern


def test_units_by_entity_and_alias_match() -> None:
    db = DeviceDB()

    modern = db.units_by_entity("Voltage")
    legacy = db.unitsByEntity("Voltage")

    assert modern == legacy
    assert modern[0][1] == "Voltage"

