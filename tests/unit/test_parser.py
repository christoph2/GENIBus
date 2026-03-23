import pytest

from genibus.linklayer import parser
from genibus.utils import crc


def test_parse_frame_valid_crc_vector() -> None:
    frame = (0x27, 0x07, 0x20, 0x01, 0x02, 0xC3, 0x02, 0x10, 0x1A, 0x90, 0x1C)

    parsed = parser.parse_frame(frame)

    assert parsed.sd.value == 0x27
    assert parsed.da == 0x20
    assert parsed.sa == 0x01
    assert len(parsed.APDUs) == 1


def test_parse_alias_points_to_snake_case() -> None:
    frame = (0x27, 0x07, 0x20, 0x01, 0x02, 0xC3, 0x02, 0x10, 0x1A, 0x90, 0x1C)

    parsed_a = parser.parse(frame)
    parsed_b = parser.parse_frame(frame)

    assert parsed_a == parsed_b


def test_parse_frame_rejects_short_frame() -> None:
    with pytest.raises(parser.FramingError):
        parser.parse_frame((0x27, 0x01, 0x20, 0x01, 0x00))


def test_parse_frame_rejects_unknown_apdu_class() -> None:
    base = bytearray([0x27, 0x04, 0x20, 0x01, 0x0E, 0x00])
    frame = crc.append_tel(base)

    with pytest.raises(parser.APDUClassNotSupportedError):
        parser.parse_frame(frame)


def test_dissect_alias_points_to_snake_case() -> None:
    old_result = parser.dissectPumpStatus("act_mode1", 0x00)
    new_result = parser.dissect_pump_status("act_mode1", 0x00)

    assert old_result == new_result

