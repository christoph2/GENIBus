import genibus.gbdefs as defs


def test_snake_case_constant_aliases_match_legacy() -> None:
    assert defs.start_delimiter == defs.START_DELIMITER
    assert defs.length == defs.LENGTH
    assert defs.destination_address == defs.DESTINATION_ADRESS
    assert defs.source_address == defs.SOURCE_ADDRESS
    assert defs.pdu_start == defs.PDU_START
    assert defs.crc_high == defs.CRC_HIGH
    assert defs.crc_low == defs.CRC_LOW
    assert defs.max_telegram_len == defs.MAX_TELEGRAM_LEN
    assert defs.max_pdu_len == defs.MAX_PDU_LEN
    assert defs.slave_addr_offset == defs.SLAVE_ADDR_OFFSET
    assert defs.connection_req_addr == defs.CONNECTION_REQ_ADDR
    assert defs.broadcast_addr == defs.BROADCAST_ADDR


def test_snake_case_mapping_aliases_match_legacy() -> None:
    assert defs.nice_class_names is defs.NICE_CLASS_NAMES
    assert defs.class_capabilities is defs.CLASS_CAPABILITIES


def test_dataclasses_still_work() -> None:
    info = defs.Info(head="Header", unit="V", zero=0.0, range=10.0)
    item = defs.Item(name="v_dc", value=27, info=info)

    assert item.info.unit == "V"
    assert item.value == 27

