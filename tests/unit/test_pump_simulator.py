import pytest

import genibus.gbdefs as defs
from genibus.linklayer import parser
from genibus.utils import crc
from tools.pump_sim.simulator import PumpSimulator, PumpState


def _build_request(
    da: int,
    sa: int,
    klass: defs.APDUClass,
    op: defs.Operation,
    data: list[int],
) -> bytearray:
    frame = [
        defs.FrameType.SD_DATA_REQUEST,
        0,
        da,
        sa,
        int(klass),
        ((int(op) << 6) | len(data)) & 0xFF,
    ]
    frame.extend(data)
    frame[defs.LENGTH] = len(frame) - 2
    return bytearray(crc.append_tel(frame))


def _class_item_ids(klass: defs.APDUClass) -> dict[str, int]:
    from tools.pump_sim import simulator as sim

    mapping = sim.DATA_BY_CLASS[klass]
    return {name: item_id for item_id, (name, _acc, _note) in mapping.items()}


def test_process_frame_get_and_connect_address_mapping() -> None:
    state = PumpState()
    sim = PumpSimulator(state=state)
    measured_ids = _class_item_ids(defs.APDUClass.MEASURED_DATA)
    req = _build_request(
        defs.CONNECTION_REQ_ADDR,
        0x01,
        defs.APDUClass.MEASURED_DATA,
        defs.Operation.GET,
        [measured_ids["h"], measured_ids["q"]],
    )

    resp = sim.process_frame(req)
    parsed = parser.parse(resp)

    assert parsed.sd == defs.FrameType.SD_DATA_REPLY
    assert parsed.da == 0x01
    assert parsed.sa == state.unit_addr
    assert len(parsed.APDUs) == 1
    assert parsed.APDUs[0].klass == defs.APDUClass.MEASURED_DATA
    assert parsed.APDUs[0].ack == defs.Operation.GET
    assert len(parsed.APDUs[0].data) == 2


def test_process_frame_set_ack_and_updates_value() -> None:
    state = PumpState()
    sim = PumpSimulator(state=state)
    ref_ids = _class_item_ids(defs.APDUClass.REFERENCE_VALUES)
    measured_ids = _class_item_ids(defs.APDUClass.MEASURED_DATA)

    set_req = _build_request(
        0x20,
        0x01,
        defs.APDUClass.REFERENCE_VALUES,
        defs.Operation.SET,
        [ref_ids["ref_rem"], 60],
    )
    set_resp = sim.process_frame(set_req)
    set_parsed = parser.parse(set_resp)

    assert len(set_parsed.APDUs) == 1
    assert set_parsed.APDUs[0].klass == defs.APDUClass.REFERENCE_VALUES
    assert set_parsed.APDUs[0].ack == defs.Operation.GET
    assert set_parsed.APDUs[0].data == []
    assert state.ref_rem == 60

    get_req = _build_request(
        0x20,
        0x01,
        defs.APDUClass.MEASURED_DATA,
        defs.Operation.GET,
        [measured_ids["ref_act"]],
    )
    get_resp = sim.process_frame(get_req)
    get_parsed = parser.parse(get_resp)

    assert get_parsed.APDUs[0].data == [60]


def test_process_frame_info_has_expected_payload_shape() -> None:
    sim = PumpSimulator(state=PumpState())
    measured_ids = _class_item_ids(defs.APDUClass.MEASURED_DATA)
    req = _build_request(
        0x20,
        0x01,
        defs.APDUClass.MEASURED_DATA,
        defs.Operation.INFO,
        [measured_ids["h"], measured_ids["speed_lo"]],
    )

    resp = sim.process_frame(req)
    parsed = parser.parse(resp)

    # h -> 4 Byte INFO, speed_lo -> 1 Byte INFO
    assert len(parsed.APDUs) == 1
    assert parsed.APDUs[0].ack == defs.Operation.GET
    assert len(parsed.APDUs[0].data) == 5


def test_process_frame_rejects_invalid_operation_code() -> None:
    sim = PumpSimulator(state=PumpState())
    measured_ids = _class_item_ids(defs.APDUClass.MEASURED_DATA)

    frame = [
        defs.FrameType.SD_DATA_REQUEST,
        0,
        0x20,
        0x01,
        int(defs.APDUClass.MEASURED_DATA),
        (1 << 6) | 1,
        measured_ids["h"],
    ]
    frame[defs.LENGTH] = len(frame) - 2
    req = bytearray(crc.append_tel(frame))

    with pytest.raises(defs.IllegalOperationError):
        sim.process_frame(req)


def test_process_frame_rejects_odd_set_payload() -> None:
    sim = PumpSimulator(state=PumpState())
    ref_ids = _class_item_ids(defs.APDUClass.REFERENCE_VALUES)
    req = _build_request(
        0x20,
        0x01,
        defs.APDUClass.REFERENCE_VALUES,
        defs.Operation.SET,
        [ref_ids["ref_rem"], 50, ref_ids["ref_ir"]],
    )

    with pytest.raises(parser.FramingError):
        sim.process_frame(req)


def test_process_frame_rejects_bad_crc() -> None:
    sim = PumpSimulator(state=PumpState())
    measured_ids = _class_item_ids(defs.APDUClass.MEASURED_DATA)
    req = _build_request(
        0x20,
        0x01,
        defs.APDUClass.MEASURED_DATA,
        defs.Operation.GET,
        [measured_ids["h"]],
    )
    req[-1] ^= 0xFF

    with pytest.raises(crc.CrcError):
        sim.process_frame(req)


class _FakeSession:
    def __init__(self, frames: list[bytearray]) -> None:
        self._frames = list(frames)
        self.sent: list[bytearray] = []
        self.closed = False

    def recv_frame(self) -> bytearray:
        if not self._frames:
            return bytearray()
        return self._frames.pop(0)

    def send_frame(self, frame: bytearray) -> None:
        self.sent.append(frame)

    def close(self) -> None:
        self.closed = True


def test_serve_session_processes_until_eof_and_closes() -> None:
    sim = PumpSimulator(state=PumpState())
    measured_ids = _class_item_ids(defs.APDUClass.MEASURED_DATA)
    req = _build_request(
        0x20,
        0x01,
        defs.APDUClass.MEASURED_DATA,
        defs.Operation.GET,
        [measured_ids["h"]],
    )
    session = _FakeSession([req, req, bytearray()])

    sim.serve_session(session)

    assert session.closed is True
    assert len(session.sent) == 2
