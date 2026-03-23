from genibus.linklayer import parser


def _as_dict(entries):
    return {key: value for key, value in entries}


def test_dissect_pump_status_act_mode1() -> None:
    # operationMode=Max (3), controlMode=Constant Frequency (2), nightReduction=1
    decoded = _as_dict(parser.dissect_pump_status("act_mode1", 0x53))

    assert decoded["nightReduction"] == 1
    assert decoded["operationMode"] == "Max"
    assert decoded["controlMode"] == "Constant Frequency"


def test_dissect_pump_status_act_mode2() -> None:
    # temperatureInfluence=1, buttonsOnPump=1, minimumCurve=3
    decoded = _as_dict(parser.dissect_pump_status("act_mode2", 0xE1))

    assert decoded["temperatureInfluence"] == 1
    assert decoded["buttonsOnPump"] == 1
    assert decoded["minimumCurve"] == 3


def test_dissect_pump_status_act_mode3() -> None:
    # systemMode=Alarm Standby (4), pendingAlarm=1, sourceMode=Local
    decoded = _as_dict(parser.dissect_pump_status("act_mode3", 0x1C))

    assert decoded["systemMode"] == "Alarm Standby"
    assert decoded["pendingAlarm"] == 1
    assert decoded["sourceMode"] == "Local"


def test_dissect_pump_status_contr_source_decodes_high_nibble() -> None:
    # upper nibble 0x2 => GENIBus
    decoded = _as_dict(parser.dissect_pump_status("contr_source", 0x20))

    assert decoded["activeSource"] == "GENIBus"


def test_dissect_pump_status_alias_matches_snake_case() -> None:
    old_result = parser.dissectPumpStatus("act_mode2", 0xE1)
    new_result = parser.dissect_pump_status("act_mode2", 0xE1)

    assert old_result == new_result

