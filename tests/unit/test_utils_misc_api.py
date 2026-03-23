import logging

from genibus.utils import bytes as byte_utils
from genibus.utils.locales import getLocalCode, get_locale_code
from genibus.utils.logger import Logger


def test_bytes_snake_case_and_legacy_aliases() -> None:
    assert byte_utils.make_word(0x12, 0x34) == 0x1234
    assert byte_utils.makeWord(0x12, 0x34) == 0x1234
    assert byte_utils.hi_byte(0xABCD) == 0xAB
    assert byte_utils.hiByte(0xABCD) == 0xAB
    assert byte_utils.lo_byte(0xABCD) == 0xCD
    assert byte_utils.loByte(0xABCD) == 0xCD
    assert byte_utils.to_bytes(0xABCD) == (0xAB, 0xCD)
    assert byte_utils.toBytes(0xABCD) == (0xAB, 0xCD)
    assert tuple(byte_utils.make_buffer([1, 2, 3])) == (1, 2, 3)
    assert byte_utils.make_array(bytearray([1, 2, 3])) == (1, 2, 3)
    assert byte_utils.dump_hex([16, 32]) == ["0x10", "0x20"]
    assert byte_utils.dumpHex([16, 32]) == ["0x10", "0x20"]


def test_locale_code_snake_case_and_legacy_aliases() -> None:
    assert get_locale_code(1031) == "de-DE"
    assert getLocalCode(1031) == "de-DE"
    assert get_locale_code(999999) == "?"


def test_logger_api_aliases() -> None:
    logger = Logger(level=logging.INFO)

    logger.info("hello")
    severity, message = logger.get_last_error()
    assert severity == logging.INFO
    assert message == "hello"

    logger.warn("warning")
    severity2, message2 = logger.getLastError()
    assert severity2 == logging.WARN
    assert message2 == "warning"

    logger.set_level("debug")
    assert logger.logger.level == logging.DEBUG

    logger.setLevel("ERROR")
    assert logger.logger.level == logging.ERROR

