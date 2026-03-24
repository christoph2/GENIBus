#!/usr/bin/env python

__version__ = "0.1.0"

__copyright__ = """
Grundfos GENIBus Library.

(C) 2007-2017 by Christoph Schueler <github.com/Christoph2,
                                     cpu12.gems@googlemail.com>

 All Rights Reserved

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""


import logging
from collections import namedtuple
from collections.abc import Sequence

import genibus.gbdefs as defs
import genibus.utils.crc as crc

logger = logging.getLogger("GeniControl")

## dissecting states.
APDU_HEADER0    = 0
APDU_HEADER1    = 1
APDU_DATA       = 2

APDU = namedtuple('APDU', 'klass ack data')
ParseResult = namedtuple('ParseResult', 'sd da sa APDUs')
StatusValue = int | str
StatusEntry = tuple[str, StatusValue]


class APDUClassNotSupportedError(Exception):
    pass


# Backward-compatible alias for historic typo.
ADPUClassNotSupportedError = APDUClassNotSupportedError


class FramingError(Exception):
    pass

def parse_frame(frame: Sequence[int]) -> ParseResult:
#    arr = tuple([ord(x) for x in frame])
    arr = tuple(frame)

    if len(arr) < 6:
        raise FramingError("Frame too short.")

    crc.check_tel(frame)
    sd = arr[defs.START_DELIMITER]
    length = arr[defs.LENGTH]
    da = arr[defs.DESTINATION_ADDRESS]
    sa = arr[defs.SOURCE_ADDRESS]

    dissectingState = APDU_HEADER0
    byteCount = 0
    result: list[APDU] = []

    valid_apdu_classes = tuple(item.value for item in defs.APDUClass)

    if not (length == len(arr) - 4):
        raise FramingError("Frame length doesn't match length byte.")
    for idx in range(defs.PDU_START, length + 2):
        ch = arr[idx]
        if dissectingState == APDU_HEADER0:
            klass = ch & 0x0f
            if klass not in valid_apdu_classes:
                raise APDUClassNotSupportedError(
                    f"APDU class '{klass}' not supported by GeniControl."
                )
            dissectingState = APDU_HEADER1
            data: list[int] = []
        elif dissectingState == APDU_HEADER1:
            numberOfDataBytes = ch & 0x3F
            opAck = (ch & 0xC0) >> 6
            byteCount = numberOfDataBytes
            if byteCount:
                dissectingState = APDU_DATA
            else:
                dissectingState = APDU_HEADER0
                result.append(APDU(klass, opAck, data))
        elif dissectingState == APDU_DATA:
            byteCount -= 1
            data.append(ch)
            if byteCount <= 0:
                dissectingState = APDU_HEADER0
                result.append(APDU(klass, opAck, data))

    if dissectingState != APDU_HEADER0:
        raise FramingError("Incomplete APDU payload in frame.")

    return ParseResult(defs.FrameType(sd), da, sa, result)


def parse(frame: Sequence[int]) -> ParseResult:
    return parse_frame(frame)



def dissect_pump_status(dp: str, value: int) -> list[StatusEntry]:
    result: list[StatusEntry] = []
    if dp == 'act_mode1':
        operationMode = (value & 0x7)
        controlMode = (value & 0x38) >> 3
        nightReduction = (value & 0x40) >> 6

        result.append(('nightReduction', nightReduction, ))
        if operationMode == 0x00:
            om = 'Start'
        elif operationMode == 0x01:
            om = 'Stop'
        elif operationMode == 0x02:
            om = 'Min'
        elif operationMode == 0x03:
            om = 'Max'
        else:
            logger.info('FIX-ME: operationMode "%u"', operationMode)

        result.append(('operationMode', om, ))

        if controlMode == 0x00:
            cm = 'Constant Pressure'
        elif controlMode == 0x01:
            cm = 'Proportional Pressure'
        elif controlMode == 0x02:
            cm = 'Constant Frequency'
        elif controlMode == 0x05:
            cm = 'Automatic Setpoint'
        result.append(('controlMode', cm, ))
    elif dp == 'act_mode2':
        temperatureInfluence = value & 0x01
        buttonsOnPump = (value & 0x20) >> 5
        minimumCurve = (value & 0xc0) >> 6
        result.append(('temperatureInfluence', temperatureInfluence))
        result.append(('buttonsOnPump', buttonsOnPump))
        result.append(('minimumCurve', minimumCurve))
    elif dp == 'act_mode3':
        sm = value & 0x07
        if sm == 0:
            systemMode = 'Normal'
        elif sm == 3:
            systemMode = 'Survive'
        elif sm == 4:
            systemMode = 'Alarm Standby'
        else:
            systemMode = '???'
        result.append(('systemMode', systemMode))
        pendingAlarm = (value & 0x08) >> 3
        result.append(('pendingAlarm', pendingAlarm))
        sm = (value & 0x10) >> 4
        sourceMode = 'Local' if sm == 1 else 'Remote'
        result.append(('sourceMode', sourceMode))
    elif dp == 'contr_source':
        cs = (value & 0xF0) >> 4
        if cs == 0b0001:
            contrSource = "Buttons"
        elif cs == 0b0010:
            contrSource = "GENIBus"
        elif cs == 0b0011:
            contrSource = "GENILink"
        elif cs == 0b0100:
            contrSource = "External control"
        else:
            contrSource = 'Buttons' # ???
        result.append(('activeSource', contrSource))
    return result


def dissectPumpStatus(dp: str, value: int) -> list[StatusEntry]:
    return dissect_pump_status(dp, value)

def main() -> None:
    pass


if __name__ == '__main__':
    main()

