#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

from genibus.devices.db import DeviceDB
import genibus.gbdefs as defs
import genibus.utils.crc as crc

logger = logging.getLogger("Genibus")

db = DeviceDB()

DatapointValue = Tuple[str, int]

def createAPDUHeader(apdu: List[int], klass: int, operationSpecifier: int, length: int) -> None:
    apdu.append(klass)
    apdu.append((operationSpecifier << 6) | (length & 0x3F))


def createAPDU(klass: int, op: int, datapoints: Sequence[DatapointValue]) -> List[int]:
    di = db.dataitemsByClass("magna", klass)
    result: List[int] = []
    createAPDUHeader(result, klass, op, len(datapoints) * 2)
    for dp, value in datapoints:
        item = di[dp]
        result.append(item.id)
        result.append(value)
    return result


def createAPDUNoData(klass: int, op: int, datapoints: Sequence[str]) -> List[int]:
    di = db.dataitemsByClass("magna", klass)
    result: List[int] = []
    createAPDUHeader(result, klass, op, len(datapoints))
    for dp in datapoints:
        item = di[dp]
        result.append(item.id)
    return result

def createGetInfoAPDU(klass: int, datapoints: Sequence[str]) -> List[int]:
    result = createAPDUNoData(klass, defs.Operation.INFO, datapoints)
    return result

def createGetMeasuredDataAPDU(klass: int, datapoints: Sequence[str]) -> List[int]:
    result = createAPDUNoData(klass, defs.Operation.GET, datapoints)
    return result

def createSetCommandsAPDU(datapoints: Sequence[str]) -> List[int]:
    result = createAPDUNoData(defs.APDUClass.COMMANDS, defs.Operation.SET, datapoints)
    return result

def createGetReferencesAPDU(datapoints: Sequence[str]) -> List[int]:
    result = createAPDUNoData(defs.APDUClass.REFERENCE_VALUES, defs.Operation.GET, datapoints)
    return result

def createSetReferencesAPDU(datapoints: Sequence[DatapointValue]) -> List[int]:
    result = createAPDU(defs.APDUClass.REFERENCE_VALUES, defs.Operation.SET, datapoints)
    return result

def createGetStringsAPDU(datapoints: Sequence[str]) -> List[int]:
    result = createAPDUNoData(defs.APDUClass.ASCII_STRINGS, defs.Operation.GET, datapoints)
    return result

def createGetParametersAPDU(datapoints: Sequence[str]) -> List[int]:
    result = createAPDUNoData(defs.APDUClass.CONFIGURATION_PARAMETERS, defs.Operation.GET, datapoints)
    return result

def createSetParametersAPDU(datapoints: Sequence[DatapointValue]) -> List[int]:
    result = createAPDU(defs.APDUClass.CONFIGURATION_PARAMETERS, defs.Operation.SET, datapoints)
    return result

def createGetProtocolDataAPDU(datapoints: Sequence[str]) -> List[int]:
    result = createAPDUNoData(defs.APDUClass.PROTOCOL_DATA, defs.Operation.GET, datapoints)
    return result


@dataclass(frozen=True)
class Header(object):
    startDelimiter: int
    destAddr: int
    sourceAddr: int


def createGetValuesPDU(
    klass: int,
    header: Header,
    protocolData: Optional[Sequence[str]] = None,
    measurements: Optional[Sequence[str]] = None,
    parameter: Optional[Sequence[str]] = None,
    references: Optional[Sequence[str]] = None,
    strings: Optional[Sequence[str]] = None,
) -> bytearray:
    if not isinstance(header, Header):
        raise TypeError('Parameter "header" must be of type "Header".')

    protocolData = list(protocolData or [])
    measurements = list(measurements or [])
    parameter = list(parameter or [])
    references = list(references or [])
    strings = list(strings or [])

    length = 2
    pdu = bytearray()

    if protocolData:
        protocolAPDU = createGetProtocolDataAPDU(protocolData)
        length += len(protocolAPDU)

    if measurements:
        measurementAPDU = createGetMeasuredDataAPDU(klass, measurements)
        length += len(measurementAPDU)

    if parameter:
        parameterAPDU = createGetParametersAPDU(parameter)
        length += len(parameterAPDU)

    if references:
        referencesAPDU = createGetReferencesAPDU(references)
        length += len(referencesAPDU)

    if strings:
        stringsAPDU = createGetStringsAPDU(strings)
        length += len(stringsAPDU )

    pdu.extend([header.startDelimiter, length, header.destAddr, header.sourceAddr])

    if protocolData:
        pdu.extend(protocolAPDU)

    if parameter:
        pdu.extend(parameterAPDU)

    if measurements:
        pdu.extend(measurementAPDU)

    if references:
        pdu.extend(referencesAPDU)

    if strings:
        pdu.extend(stringsAPDU)

    pdu = crc.append_tel(pdu)

    return pdu


def createSetValuesPDU(
    header: Header,
    parameter: Optional[Sequence[DatapointValue]] = None,
    references: Optional[Sequence[DatapointValue]] = None,
) -> bytearray:
    if not isinstance(header, Header):
        raise TypeError('Parameter "header" must be of type "Header".')

    parameter = list(parameter or [])
    references = list(references or [])

    length = 2
    pdu = bytearray()

    if parameter:
        parameterAPDU = createSetParametersAPDU(parameter)
        length += len(parameterAPDU)

    if references:
        referencesAPDU = createSetReferencesAPDU(references)
        length += len(referencesAPDU)

    pdu.extend([header.startDelimiter, length, header.destAddr, header.sourceAddr])

    if parameter:
        pdu.extend(parameterAPDU)

    if references:
        pdu.extend(referencesAPDU)

    pdu = crc.append_tel(pdu)

    return pdu


def createGetInfoPDU(
    klass: int,
    header: Header,
    measurements: Optional[Sequence[str]] = None,
    parameter: Optional[Sequence[str]] = None,
    references: Optional[Sequence[str]] = None,
) -> bytearray:
    ## To be defensive, at most 15 datapoints should be requested at once (min.frame length = 70 bytes).
    if not isinstance(header, Header):
        raise TypeError('Parameter "header" must be of type "Header".')

    measurements = list(measurements or [])
    parameter = list(parameter or [])
    references = list(references or [])

    length = 2
    pdu = bytearray()
    if measurements:
        measurementsAPDU: List[int]
        if klass == defs.APDUClass.MEASURED_DATA:
            measurementsAPDU = createGetInfoAPDU(defs.APDUClass.MEASURED_DATA, measurements)
        elif klass == defs.APDUClass.SIXTEENBIT_MEASURED_DATA:
            measurementsAPDU = createGetInfoAPDU(defs.APDUClass.SIXTEENBIT_MEASURED_DATA, measurements)
        else:
            raise ValueError("Invalid APDU class for measurements info request: %r" % (klass, ))
        length += len(measurementsAPDU)

    if parameter:
        parameterAPDU = createGetInfoAPDU(defs.APDUClass.CONFIGURATION_PARAMETERS, parameter)
        length += len(parameterAPDU)

    if references:
        referencesAPDU = createGetInfoAPDU(defs.APDUClass.REFERENCE_VALUES, references)
        length += len(referencesAPDU)

    pdu.extend([header.startDelimiter, length, header.destAddr, header.sourceAddr])

    if measurements:
        pdu.extend(measurementsAPDU)

    if parameter:
        pdu.extend(parameterAPDU)

    if references:
        pdu.extend(referencesAPDU)

    pdu = crc.append_tel(pdu)

    return pdu


def createSetCommandsPDU(header: Header, commands: Sequence[str]) -> bytearray:
    if not isinstance(header, Header):
        raise TypeError('Parameter "header" must be of type "Header".')

    length = 2
    pdu = bytearray()

    commandsAPDU = createSetCommandsAPDU(commands)
    length += len(commandsAPDU)

    pdu.extend([header.startDelimiter, length, header.destAddr, header.sourceAddr])

    pdu.extend(commandsAPDU)

    pdu = crc.append_tel(pdu)

    return pdu



def createConnectRequestPDU(sourceAddr: int) -> bytearray:
    return createGetValuesPDU(2,
        Header(defs.FrameType.SD_DATA_REQUEST, defs.CONNECTION_REQ_ADDR, sourceAddr),
        measurements =  ['unit_family', 'unit_type'],
        protocolData =  ['buf_len', 'unit_bus_mode'],
        parameter =     ['unit_addr',  'group_addr']
    )


def createSetRemotePDU(sourceAddr: int) -> bytearray:
    return createSetCommandsPDU(
        Header(defs.FrameType.SD_DATA_REQUEST, 0x20, sourceAddr),
        commands = ['REMOTE']
    )


def create_apdu_header(apdu: List[int], klass: int, operation_specifier: int, length: int) -> None:
    createAPDUHeader(apdu, klass, operation_specifier, length)


def create_apdu(klass: int, op: int, datapoints: Sequence[DatapointValue]) -> List[int]:
    return createAPDU(klass, op, datapoints)


def create_apdu_no_data(klass: int, op: int, datapoints: Sequence[str]) -> List[int]:
    return createAPDUNoData(klass, op, datapoints)


def create_get_info_apdu(klass: int, datapoints: Sequence[str]) -> List[int]:
    return createGetInfoAPDU(klass, datapoints)


def create_get_measured_data_apdu(klass: int, datapoints: Sequence[str]) -> List[int]:
    return createGetMeasuredDataAPDU(klass, datapoints)


def create_set_commands_apdu(datapoints: Sequence[str]) -> List[int]:
    return createSetCommandsAPDU(datapoints)


def create_get_references_apdu(datapoints: Sequence[str]) -> List[int]:
    return createGetReferencesAPDU(datapoints)


def create_set_references_apdu(datapoints: Sequence[DatapointValue]) -> List[int]:
    return createSetReferencesAPDU(datapoints)


def create_get_strings_apdu(datapoints: Sequence[str]) -> List[int]:
    return createGetStringsAPDU(datapoints)


def create_get_parameters_apdu(datapoints: Sequence[str]) -> List[int]:
    return createGetParametersAPDU(datapoints)


def create_set_parameters_apdu(datapoints: Sequence[DatapointValue]) -> List[int]:
    return createSetParametersAPDU(datapoints)


def create_get_protocol_data_apdu(datapoints: Sequence[str]) -> List[int]:
    return createGetProtocolDataAPDU(datapoints)


def create_get_values_pdu(
    klass: int,
    header: Header,
    protocol_data: Optional[Sequence[str]] = None,
    measurements: Optional[Sequence[str]] = None,
    parameter: Optional[Sequence[str]] = None,
    references: Optional[Sequence[str]] = None,
    strings: Optional[Sequence[str]] = None,
) -> bytearray:
    return createGetValuesPDU(
        klass,
        header,
        protocolData=protocol_data,
        measurements=measurements,
        parameter=parameter,
        references=references,
        strings=strings,
    )


def create_set_values_pdu(
    header: Header,
    parameter: Optional[Sequence[DatapointValue]] = None,
    references: Optional[Sequence[DatapointValue]] = None,
) -> bytearray:
    return createSetValuesPDU(header, parameter=parameter, references=references)


def create_get_info_pdu(
    klass: int,
    header: Header,
    measurements: Optional[Sequence[str]] = None,
    parameter: Optional[Sequence[str]] = None,
    references: Optional[Sequence[str]] = None,
) -> bytearray:
    return createGetInfoPDU(
        klass,
        header,
        measurements=measurements,
        parameter=parameter,
        references=references,
    )


def create_set_commands_pdu(header: Header, commands: Sequence[str]) -> bytearray:
    return createSetCommandsPDU(header, commands)


def create_connect_request_pdu(source_addr: int) -> bytearray:
    return createConnectRequestPDU(source_addr)


def create_set_remote_pdu(source_addr: int) -> bytearray:
    return createSetRemotePDU(source_addr)


