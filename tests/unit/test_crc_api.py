import pytest

from genibus.utils import crc


def test_append_telegram_matches_legacy_alias() -> None:
    base = bytearray([0x27, 0x04, 0x20, 0x01, 0x00, 0x00])

    modern = crc.append_telegram(base)
    legacy = crc.append_tel(base)

    assert modern == legacy


def test_check_telegram_matches_legacy_alias() -> None:
    frame = (0x27, 0x07, 0x20, 0x01, 0x02, 0xC3, 0x02, 0x10, 0x1A, 0x90, 0x1C)

    assert crc.check_telegram(frame)
    assert crc.check_tel(frame)


def test_calculate_crc_aliases_match() -> None:
    payload = bytearray([0x07, 0x20, 0x01, 0x02, 0xC3, 0x02, 0x10, 0x1A])

    assert crc.calculate_crc(payload) == crc.calc_raw(payload)


def test_frame_crc_aliases_match() -> None:
    frame = (0x27, 0x07, 0x20, 0x01, 0x02, 0xC3, 0x02, 0x10, 0x1A, 0x90, 0x1C)

    assert crc.check_crc(frame) == crc.checkCrc(frame)
    assert crc.calculate_frame_crc(frame) == crc.calcuteCrc(frame)


def test_check_telegram_raises_on_invalid_crc() -> None:
    broken = bytearray([0x27, 0x07, 0x20, 0x01, 0x02, 0xC3, 0x02, 0x10, 0x1A, 0x90, 0x00])

    with pytest.raises(crc.CrcError):
        crc.check_telegram(broken)

    assert crc.check_telegram(broken, silent=True) is False

