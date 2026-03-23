import pytest

import genibus.apdu as apdu
import genibus.gbdefs as defs


def test_create_get_info_pdu_rejects_invalid_measurement_class() -> None:
    header = apdu.Header(defs.FrameType.SD_DATA_REQUEST, 0x20, 0x01)

    with pytest.raises(ValueError):
        apdu.create_get_info_pdu(
            klass=defs.APDUClass.CONFIGURATION_PARAMETERS,
            header=header,
            measurements=["h"],
        )


def test_create_get_info_pdu_allows_valid_measurement_class() -> None:
    header = apdu.Header(defs.FrameType.SD_DATA_REQUEST, 0x20, 0x01)

    pdu_8bit = apdu.create_get_info_pdu(
        klass=defs.APDUClass.MEASURED_DATA,
        header=header,
        measurements=["h"],
    )

    assert isinstance(pdu_8bit, bytearray)

