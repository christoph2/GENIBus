from genibus.utils import helper


def test_hex_dump_matches_legacy_alias() -> None:
    data = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x00"
    expected = "0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x00"

    assert helper.hex_dump(data) == expected
    assert helper.hexDump(data) == expected

