/*
 *  Grundfos GENIBus Library.
 *
 *  (C) 2007-2016 by Christoph Schueler <github.com/Christoph2,
 *                                       cpu12.gems@googlemail.com>
 *
 *   All Rights Reserved
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License along
 *  with this program; if not, write to the Free Software Foundation, Inc.,
 *  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 *
 */

#include "genibus/datalink.h"
#include <stdio.h>

static const uint8 connectReqPayload[] = {
    0x00, 0x02, 0x02, 0x03, 0x04, 0x02, 0x2e, 0x2f, 0x02, 0x02, 0x94, 0x95
};


void GB_Datalink::sendPDU(uint8 sd, uint8 da, uint8 sa, uint8 const * data, uint8 len)
{
    uint8 _idx;
    uint16 calculatedCrc;

    if (getState() != DL_IDLE) {
        return;
    }

    setState(DL_SENDING);

    _scratchBuffer[0] = sd;
    _scratchBuffer[1] = len + ((uint8)0x02);
    _scratchBuffer[2] = da;
    _scratchBuffer[3] = sa;

    for (_idx = ((uint8)0x00); _idx < len; ++_idx) {
        _scratchBuffer[_idx + ((uint8)0x04)] = data[_idx];
    }

    calculatedCrc = calculateCRC(1, len + 4);
    _scratchBuffer[_idx] = HIBYTE(calculatedCrc);
    _scratchBuffer[_idx + 1] = LOBYTE(calculatedCrc);

    _port.write(_scratchBuffer, len);

    setState(DL_IDLE);
}

void GB_Datalink::sendRaw(uint8 const * data, uint8 len)
{
    _port.write(data, len);
}


void GB_Datalink::write(uint8 ch)
{
    _port.write(ch);
}


/*!
 *  TODO: Callback 'onError(code)'.
 */

typedef enum tagDl_Error {
    DL_ERROR_NONE,
    DL_ERROR_TIMEOUT,
    DL_ERROR_CHECKSUM
};

void GB_Datalink::reset(void)
{
    _idx = 0;
    setState(DL_IDLE);
}

void GB_Datalink::feed(void)
{
    static uint8 byteCount;
    uint8 receivedByte;
    uint16 calculatedCrc;

    while (_port.available() > 0) {
        receivedByte = _port.read();
        _scratchBuffer[_idx] = receivedByte;
        if (_idx == 1) {
            byteCount =  receivedByte + 3;
            _frameLength = byteCount + 1;
            setState(DL_RECEIVING);
        } else if (_idx == 0) {
           // printf("START.\n");
        }
        if (getState() == DL_RECEIVING) {
            //printf("%u\n", byteCount);
            if (--byteCount == 0) {
                if (verifyCRC(1, _frameLength - 2)) {
                    if (_dataLinkCallout != NULL) {
                        _dataLinkCallout(_scratchBuffer, _frameLength);
                    }
                } else {
                    if (_errorCallout != NULL) {
                        _errorCallout(ERR_INVALID_CRC, _scratchBuffer, _frameLength);
                    }
                }
                setState(DL_IDLE);
                _idx = 0;
                break; /* We're done. */
            }
        }
        ++_idx;
    }
}

void GB_Datalink::connectRequest(uint8 sa)
{
   sendPDU(0x27, 0xfe, sa, connectReqPayload, ARRAY_SIZE(connectReqPayload));
}

uint16  GB_Datalink::calculateCRC(uint8 leftBound, uint8 rightBound)
{
    uint8 _idx;

     _crc.init(0xffff);

    for (_idx = leftBound; _idx < rightBound; ++_idx) {
        _crc.update(_scratchBuffer[_idx]);
    }

    return _crc.get();
}

bool GB_Datalink::verifyCRC(uint8 leftBound, uint8 rightBound)
{
    uint16 calculatedCrc;
    uint16 receivedCrc;

    receivedCrc = MAKEWORD(_scratchBuffer[rightBound], _scratchBuffer[rightBound + 1]);
    calculatedCrc = calculateCRC(leftBound, rightBound);
    //printf("R: %#4X C: %#4X\n", receivedCrc, calculatedCrc);
    return receivedCrc == calculatedCrc;
}

