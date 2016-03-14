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


void LinkLayer_Init(DatalinkLayerType * linkLayer)
{
    LinkLayer_Reset(linkLayer);
}

void LinkLayer_Reset(DatalinkLayerType * linkLayer)
{
    LinkLayer_SetState(linkLayer, DL_IDLE);
    linkLayer->frameLength = 0;
    linkLayer->frameIdx = 0;
}

void LinkLayer_SetState(DatalinkLayerType * linkLayer, Dl_State state)
{
    linkLayer->state = state;
}

Dl_State LinkLayer_GetState(DatalinkLayerType * linkLayer)
{
    return linkLayer->state;
}

void LinkLayer_Feed(DatalinkLayerType * linkLayer)
{
    static uint8 byteCount;
    uint8 receivedByte;

    while (linkLayer->port->available() > 0) {
        receivedByte = linkLayer->port->readByte();
        linkLayer->scratchBuffer[linkLayer->frameIdx] = receivedByte;
        if (linkLayer->frameIdx == 1) {
            byteCount =  receivedByte + 3;
            linkLayer->frameLength = byteCount + 1;
            LinkLayer_SetState(linkLayer, DL_RECEIVING);
        } else if (linkLayer->frameIdx == 0) {
           // printf("START.\n");
        }
        if (LinkLayer_GetState(linkLayer) == DL_RECEIVING) {
            //printf("%u\n", byteCount);
            if (--byteCount == 0) {
                if (LinkLayer_VerifyCRC(linkLayer)) {
                    if (linkLayer->dataLinkCallout != NULL) {
                        linkLayer->dataLinkCallout(linkLayer->scratchBuffer, linkLayer->frameLength);
                    }
                } else {
                    if (linkLayer->errorCallout != NULL) {
                        linkLayer->errorCallout(ERR_INVALID_CRC, linkLayer->scratchBuffer, linkLayer->frameLength);
                    }
                }
                LinkLayer_SetState(linkLayer, DL_IDLE);
                linkLayer->frameIdx = 0;
                break; /* We're done. */
            }
        }
        ++linkLayer->frameIdx;
    }
}

boolean LinkLayer_VerifyCRC(DatalinkLayerType * linkLayer)
{
    uint16 calculatedCrc;
    uint16 receivedCrc;

    receivedCrc = MAKEWORD(linkLayer->scratchBuffer[linkLayer->frameLength - 2], linkLayer->scratchBuffer[linkLayer->frameLength - 1]);
    calculatedCrc = Crc_CalculateCRC16(linkLayer->scratchBuffer + 1, linkLayer->frameLength - 2, 0xffff);
    printf("R: %#4X C: %#4X\n", receivedCrc, calculatedCrc);
    return receivedCrc == calculatedCrc;
}

void LinkLayer_SendPDU(DatalinkLayerType * linkLayer, uint8 sd, uint8 da, uint8 sa, uint8 const * data, uint8 len)
{
    uint8 idx;
    uint16 calculatedCrc;

    if (LinkLayer_GetState(linkLayer) != DL_IDLE) {
        return;
    }

    LinkLayer_SetState(linkLayer, DL_SENDING);

    linkLayer->scratchBuffer[0] = sd;
    linkLayer->scratchBuffer[1] = len + ((uint8)0x02);
    linkLayer->scratchBuffer[2] = da;
    linkLayer->scratchBuffer[3] = sa;

    for (idx = ((uint8)0x00); idx < len; ++idx) {
        linkLayer->scratchBuffer[idx + ((uint8)0x04)] = data[idx];
    }

    calculatedCrc = Crc_CalculateCRC16(linkLayer->scratchBuffer + 1, len - 2, 0xffff);
    linkLayer->scratchBuffer[idx] = HIBYTE(calculatedCrc);
    linkLayer->scratchBuffer[idx + 1] = LOBYTE(calculatedCrc);

    linkLayer->port->writeFrame(linkLayer->scratchBuffer, len);

    LinkLayer_SetState(linkLayer, DL_IDLE);
}

void LinkLayer_ConnectRequest(DatalinkLayerType * linkLayer, uint8 sa)
{
   LinkLayer_SendPDU(linkLayer, GB_SD_REQUEST, 0xfe, sa, connectReqPayload, ARRAY_SIZE(connectReqPayload));
}

#if 0
void GB_Datalink::sendRaw(uint8 const * data, uint8 len)
{
    linkLayer->port->writeFrame(data, len);
}


void GB_Datalink::writeFrame(uint8 ch)
{
    linkLayer->port->writeFrame(ch);
}


/*!
 *  TODO: Callback 'onError(code)'.
 */


#endif

