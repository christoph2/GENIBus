#!/usr/bin/env python
"""APDU/PDU-Builder fuer GENIBus-Telegramme.

Dieses Modul stellt Builder fuer Lese-/Schreib- und Info-Telegramme bereit.
Die snake_case-Funktionen bilden die bevorzugte API; camelCase-Funktionen
bleiben als Legacy-Aliase erhalten.
"""

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
from collections.abc import Sequence
from dataclasses import dataclass

import genibus.gbdefs as defs
import genibus.utils.crc as crc
from genibus.devices.db import DeviceDB

logger = logging.getLogger("Genibus")

db = DeviceDB()

DatapointValue = tuple[str, int]

def createAPDUHeader(apdu: list[int], klass: int, operationSpecifier: int, length: int) -> None:
    apdu.append(klass)
    apdu.append((operationSpecifier << 6) | (length & 0x3F))


def createAPDU(klass: int, op: int, datapoints: Sequence[DatapointValue]) -> list[int]:
    di = db.dataitemsByClass("magna", klass)
    result: list[int] = []
    createAPDUHeader(result, klass, op, len(datapoints) * 2)
    for dp, value in datapoints:
        item = di[dp]
        result.append(item.id)
        result.append(value)
    return result


def createAPDUNoData(klass: int, op: int, datapoints: Sequence[str]) -> list[int]:
    di = db.dataitemsByClass("magna", klass)
    result: list[int] = []
    createAPDUHeader(result, klass, op, len(datapoints))
    for dp in datapoints:
        item = di[dp]
        result.append(item.id)
    return result

def createGetInfoAPDU(klass: int, datapoints: Sequence[str]) -> list[int]:
    result = createAPDUNoData(klass, defs.Operation.INFO, datapoints)
    return result

def createGetMeasuredDataAPDU(klass: int, datapoints: Sequence[str]) -> list[int]:
    result = createAPDUNoData(klass, defs.Operation.GET, datapoints)
    return result

def createSetCommandsAPDU(datapoints: Sequence[str]) -> list[int]:
    result = createAPDUNoData(defs.APDUClass.COMMANDS, defs.Operation.SET, datapoints)
    return result

def createGetReferencesAPDU(datapoints: Sequence[str]) -> list[int]:
    result = createAPDUNoData(defs.APDUClass.REFERENCE_VALUES, defs.Operation.GET, datapoints)
    return result

def createSetReferencesAPDU(datapoints: Sequence[DatapointValue]) -> list[int]:
    result = createAPDU(defs.APDUClass.REFERENCE_VALUES, defs.Operation.SET, datapoints)
    return result

def createGetStringsAPDU(datapoints: Sequence[str]) -> list[int]:
    result = createAPDUNoData(defs.APDUClass.ASCII_STRINGS, defs.Operation.GET, datapoints)
    return result

def createGetParametersAPDU(datapoints: Sequence[str]) -> list[int]:
    result = createAPDUNoData(
        defs.APDUClass.CONFIGURATION_PARAMETERS,
        defs.Operation.GET,
        datapoints,
    )
    return result

def createSetParametersAPDU(datapoints: Sequence[DatapointValue]) -> list[int]:
    result = createAPDU(defs.APDUClass.CONFIGURATION_PARAMETERS, defs.Operation.SET, datapoints)
    return result

def createGetProtocolDataAPDU(datapoints: Sequence[str]) -> list[int]:
    result = createAPDUNoData(defs.APDUClass.PROTOCOL_DATA, defs.Operation.GET, datapoints)
    return result


@dataclass(frozen=True)
class Header:
    """Telegramm-Header fuer GENIBus-PDUs."""

    startDelimiter: int
    destAddr: int
    sourceAddr: int


def createGetValuesPDU(
    klass: int,
    header: Header,
    protocolData: Sequence[str] | None = None,
    measurements: Sequence[str] | None = None,
    parameter: Sequence[str] | None = None,
    references: Sequence[str] | None = None,
    strings: Sequence[str] | None = None,
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
    parameter: Sequence[DatapointValue] | None = None,
    references: Sequence[DatapointValue] | None = None,
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
    measurements: Sequence[str] | None = None,
    parameter: Sequence[str] | None = None,
    references: Sequence[str] | None = None,
) -> bytearray:
    # At most 15 datapoints should be requested at once.
    if not isinstance(header, Header):
        raise TypeError('Parameter "header" must be of type "Header".')

    measurements = list(measurements or [])
    parameter = list(parameter or [])
    references = list(references or [])

    length = 2
    pdu = bytearray()
    if measurements:
        measurementsAPDU: list[int]
        if klass == defs.APDUClass.MEASURED_DATA:
            measurementsAPDU = createGetInfoAPDU(defs.APDUClass.MEASURED_DATA, measurements)
        elif klass == defs.APDUClass.SIXTEENBIT_MEASURED_DATA:
            measurementsAPDU = createGetInfoAPDU(
                defs.APDUClass.SIXTEENBIT_MEASURED_DATA,
                measurements,
            )
        else:
            raise ValueError(f"Invalid APDU class for measurements info request: {klass!r}")
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


def create_apdu_header(apdu: list[int], klass: int, operation_specifier: int, length: int) -> None:
    """Schreibt den zweibyten APDU-Header in den Zielpuffer.

    Args:
        apdu: Zielpuffer.
        klass: APDU-Klasse.
        operation_specifier: OP/ACK-Feld (2 Bit).
        length: Datenlaenge (6 Bit).
    """
    createAPDUHeader(apdu, klass, operation_specifier, length)


def create_apdu(klass: int, op: int, datapoints: Sequence[DatapointValue]) -> list[int]:
    """Erzeugt eine APDU mit Datapoint-ID/Wert-Paaren.

    Args:
        klass: APDU-Klasse.
        op: Operation (`defs.Operation`).
        datapoints: Sequenz aus `(name, value)`-Tupeln.

    Returns:
        list[int]: Encodierte APDU-Bytes.
    """
    return createAPDU(klass, op, datapoints)


def create_apdu_no_data(klass: int, op: int, datapoints: Sequence[str]) -> list[int]:
    """Erzeugt eine APDU ohne Datenteil (nur Datapoint-IDs).

    Args:
        klass: APDU-Klasse.
        op: Operation (`defs.Operation`).
        datapoints: Datapoint-Namen.

    Returns:
        list[int]: Encodierte APDU-Bytes.
    """
    return createAPDUNoData(klass, op, datapoints)


def create_get_info_apdu(klass: int, datapoints: Sequence[str]) -> list[int]:
    """Erzeugt eine INFO-APDU fuer die angegebene Klasse.

    Args:
        klass: APDU-Klasse.
        datapoints: Datapoint-Namen.

    Returns:
        list[int]: Encodierte APDU-Bytes.
    """
    return createGetInfoAPDU(klass, datapoints)


def create_get_measured_data_apdu(klass: int, datapoints: Sequence[str]) -> list[int]:
    """Erzeugt eine GET-APDU fuer Messdaten.

    Args:
        klass: Messdatenklasse (8/16 Bit).
        datapoints: Datapoint-Namen.

    Returns:
        list[int]: Encodierte APDU-Bytes.
    """
    return createGetMeasuredDataAPDU(klass, datapoints)


def create_set_commands_apdu(datapoints: Sequence[str]) -> list[int]:
    """Erzeugt eine SET-APDU fuer Kommando-Datapoints.

    Args:
        datapoints: Kommando-Namen.

    Returns:
        list[int]: Encodierte APDU-Bytes.
    """
    return createSetCommandsAPDU(datapoints)


def create_get_references_apdu(datapoints: Sequence[str]) -> list[int]:
    """Erzeugt eine GET-APDU fuer Referenzwerte.

    Args:
        datapoints: Referenz-Datapoint-Namen.

    Returns:
        list[int]: Encodierte APDU-Bytes.
    """
    return createGetReferencesAPDU(datapoints)


def create_set_references_apdu(datapoints: Sequence[DatapointValue]) -> list[int]:
    """Erzeugt eine SET-APDU fuer Referenzwerte.

    Args:
        datapoints: Sequenz aus `(name, value)`.

    Returns:
        list[int]: Encodierte APDU-Bytes.
    """
    return createSetReferencesAPDU(datapoints)


def create_get_strings_apdu(datapoints: Sequence[str]) -> list[int]:
    """Erzeugt eine GET-APDU fuer ASCII-String-Datapoints.

    Args:
        datapoints: Datapoint-Namen.

    Returns:
        list[int]: Encodierte APDU-Bytes.
    """
    return createGetStringsAPDU(datapoints)


def create_get_parameters_apdu(datapoints: Sequence[str]) -> list[int]:
    """Erzeugt eine GET-APDU fuer Konfigurationsparameter.

    Args:
        datapoints: Parameter-Namen.

    Returns:
        list[int]: Encodierte APDU-Bytes.
    """
    return createGetParametersAPDU(datapoints)


def create_set_parameters_apdu(datapoints: Sequence[DatapointValue]) -> list[int]:
    """Erzeugt eine SET-APDU fuer Konfigurationsparameter.

    Args:
        datapoints: Sequenz aus `(name, value)`.

    Returns:
        list[int]: Encodierte APDU-Bytes.
    """
    return createSetParametersAPDU(datapoints)


def create_get_protocol_data_apdu(datapoints: Sequence[str]) -> list[int]:
    """Erzeugt eine GET-APDU fuer Protokoll-Datapoints.

    Args:
        datapoints: Datapoint-Namen.

    Returns:
        list[int]: Encodierte APDU-Bytes.
    """
    return createGetProtocolDataAPDU(datapoints)


def create_get_values_pdu(
    klass: int,
    header: Header,
    protocol_data: Sequence[str] | None = None,
    measurements: Sequence[str] | None = None,
    parameter: Sequence[str] | None = None,
    references: Sequence[str] | None = None,
    strings: Sequence[str] | None = None,
) -> bytearray:
    """Erzeugt ein kombiniertes GET-PDU mit mehreren APDU-Segmenten.

    Args:
        klass: Messdatenklasse fuer `measurements`.
        header: Telegramm-Header.
        protocol_data: Optionale Protokoll-Datapoints.
        measurements: Optionale Messdaten-Datapoints.
        parameter: Optionale Parameter-Datapoints.
        references: Optionale Referenz-Datapoints.
        strings: Optionale ASCII-String-Datapoints.

    Returns:
        bytearray: Vollstaendiges GENIBus-Telegramm inklusive CRC.
    """
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
    parameter: Sequence[DatapointValue] | None = None,
    references: Sequence[DatapointValue] | None = None,
) -> bytearray:
    """Erzeugt ein kombiniertes SET-PDU fuer Parameter/Referenzen.

    Args:
        header: Telegramm-Header.
        parameter: Optionale Parameterwerte.
        references: Optionale Referenzwerte.

    Returns:
        bytearray: Vollstaendiges GENIBus-Telegramm inklusive CRC.
    """
    return createSetValuesPDU(header, parameter=parameter, references=references)


def create_get_info_pdu(
    klass: int,
    header: Header,
    measurements: Sequence[str] | None = None,
    parameter: Sequence[str] | None = None,
    references: Sequence[str] | None = None,
) -> bytearray:
    """Erzeugt ein INFO-PDU fuer Messdaten, Parameter und Referenzen.

    Args:
        klass: Messdatenklasse fuer `measurements`.
        header: Telegramm-Header.
        measurements: Optionale Messdaten-Datapoints.
        parameter: Optionale Parameter-Datapoints.
        references: Optionale Referenz-Datapoints.

    Returns:
        bytearray: Vollstaendiges GENIBus-Telegramm inklusive CRC.
    """
    return createGetInfoPDU(
        klass,
        header,
        measurements=measurements,
        parameter=parameter,
        references=references,
    )


def create_set_commands_pdu(header: Header, commands: Sequence[str]) -> bytearray:
    """Erzeugt ein SET-Kommando-PDU.

    Args:
        header: Telegramm-Header.
        commands: Kommando-Namen.

    Returns:
        bytearray: Vollstaendiges GENIBus-Telegramm inklusive CRC.
    """
    return createSetCommandsPDU(header, commands)


def create_connect_request_pdu(source_addr: int) -> bytearray:
    """Erzeugt ein Connect-Request-Telegramm fuer Bus-Initialisierung.

    Args:
        source_addr: Lokale Quelladresse.

    Returns:
        bytearray: Vollstaendiges Connect-Request-Telegramm.
    """
    return createConnectRequestPDU(source_addr)


def create_set_remote_pdu(source_addr: int) -> bytearray:
    """Erzeugt ein Kommando-Telegramm zum Umschalten auf Remote-Modus.

    Args:
        source_addr: Lokale Quelladresse.

    Returns:
        bytearray: Vollstaendiges Kommando-Telegramm.
    """
    return createSetRemotePDU(source_addr)


