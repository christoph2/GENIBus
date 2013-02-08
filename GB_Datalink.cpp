/*
 *  Grundfos GENIBus Library.
 *
 *  (C) 2007-2013 by Christoph Schueler <github.com/Christoph2,
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

#include "GB_Datalink.h"


static const uint8 connectReqPayload[] = {
    0x00, 0x02, 0x02, 0x03, 0x04, 0x02, 0x2e, 0x2f, 0x02, 0x02, 0x94, 0x95
};


void GB_Datalink::sendPDU(uint8 sd, uint8 da, uint8 sa, uint8 const * data, uint8 len)
{
    uint8 idx;
    uint16 calculatedCrc;

    if (getState() != DL_IDLE) {
        return;
    }

    setState(DL_SENDING);

    _scratchBuffer[0] = sd;
    _scratchBuffer[1] = len + ((uint8)0x02);
    _scratchBuffer[2] = da;
    _scratchBuffer[3] = sa;

    for (idx = ((uint8)0x00); idx < len; ++idx) {
        _scratchBuffer[idx + ((uint8)0x04)] = data[idx];
    }

    calculatedCrc = calculateCRC(1, len + 4);
    _scratchBuffer[idx] = HIBYTE(calculatedCrc);
    _scratchBuffer[idx + 1] = LOBYTE(calculatedCrc);

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

void GB_Datalink::feed(void)
{
    static uint8 idx = 0;
    static uint8 byteCount;
    uint8 receivedByte;
    uint16 calculatedCrc;

    while (Serial.available() > 0) {
        receivedByte = Serial.read();
        _scratchBuffer[idx] = receivedByte;
        if (idx == 1) {
            byteCount =  receivedByte + 2;
            _frameLength = byteCount + 1;
            setState(DL_RECEIVING);
        }
        if (getState() == DL_RECEIVING) {
            if (--byteCount == 0) {
                if (verifyCRC(1, _frameLength - 2)) {
                    if (_callout != NULL) {
                        _callout(_scratchBuffer, _frameLength);
                    }
                } else {
                    /* todo: Errorhandling! */
                }
                setState(DL_IDLE);
                idx = 0;
                break; /* We're done. */
            }
        }
        ++idx;
    }
}

void GB_Datalink::connectRequest(uint8 sa)
{
   sendPDU(0x27, 0xfe, sa, connectReqPayload, ARRAY_SIZE(connectReqPayload));
}

uint16  GB_Datalink::calculateCRC(uint8 leftBound, uint8 rightBound)
{
    uint8 idx;

     _crc.init(0xffff);

    for (idx = leftBound; idx < rightBound; ++idx) {
        _crc.update(_scratchBuffer[idx]);
    }

    return _crc.get();
}

bool GB_Datalink::verifyCRC(uint8 leftBound, uint8 rightBound)
{
    uint16 calculatedCrc;
    uint16 receivedCrc;

    receivedCrc = MAKEWORD(_scratchBuffer[rightBound + 1], _scratchBuffer[rightBound + 2]);
    calculatedCrc = calculateCRC(leftBound, rightBound);

    return receivedCrc == calculatedCrc;
}


