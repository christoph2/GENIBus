import genibus.apdu as apdu
import genibus.gbdefs as defs


def to_hex(data):
    return [item for item in data]


def test_connect_request_snake_case_matches_legacy() -> None:
    modern = apdu.create_connect_request_pdu(0x01)
    legacy = apdu.createConnectRequestPDU(0x01)

    assert to_hex(modern) == to_hex(legacy)
    assert to_hex(modern) == [
        0x27,
        0x0E,
        0xFE,
        0x01,
        0x00,
        0x02,
        0x02,
        0x03,
        0x04,
        0x02,
        0x2E,
        0x2F,
        0x02,
        0x02,
        0x94,
        0x95,
        0xA2,
        0xAA,
    ]


def test_set_commands_snake_case_matches_legacy() -> None:
    header = apdu.Header(defs.FrameType.SD_DATA_REQUEST, 0x20, 0x01)

    modern = apdu.create_set_commands_pdu(header, ["REMOTE", "START"])
    legacy = apdu.createSetCommandsPDU(header, ["REMOTE", "START"])

    assert to_hex(modern) == to_hex(legacy)
    assert to_hex(modern) == [0x27, 0x06, 0x20, 0x01, 0x03, 0x82, 0x07, 0x06, 0x07, 0xFA]


def test_get_info_snake_case_matches_legacy() -> None:
    header = apdu.Header(defs.FrameType.SD_DATA_REQUEST, 0x20, 0x01)
    datapoints = ["h", "q", "p", "t_w", "speed_hi", "energy_hi"]

    modern = apdu.create_get_info_pdu(
        klass=defs.APDUClass.MEASURED_DATA,
        header=header,
        measurements=datapoints,
    )
    legacy = apdu.createGetInfoPDU(
        klass=defs.APDUClass.MEASURED_DATA,
        header=header,
        measurements=datapoints,
    )

    assert to_hex(modern) == to_hex(legacy)
    assert to_hex(modern) == [
        0x27,
        0x0A,
        0x20,
        0x01,
        0x02,
        0xC6,
        0x25,
        0x27,
        0x22,
        0x3A,
        0x23,
        0x98,
        0x33,
        0x5A,
    ]


def test_create_get_values_pdu_accepts_snake_case_keyword_protocol_data() -> None:
    header = apdu.Header(defs.FrameType.SD_DATA_REQUEST, defs.CONNECTION_REQ_ADDR, 0x01)

    modern = apdu.create_get_values_pdu(
        2,
        header,
        protocol_data=["buf_len", "unit_bus_mode"],
        measurements=["unit_family", "unit_type"],
        parameter=["unit_addr", "group_addr"],
    )

    assert to_hex(modern) == to_hex(apdu.createConnectRequestPDU(0x01))

