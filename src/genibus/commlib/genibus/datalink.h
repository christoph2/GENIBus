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


#if !defined(__GB_DATALINK)
#define __GB_DATALINK

#if defined(__cplusplus)
extern "C"
{
#endif  /* __cplusplus */

#include "genibus/types.h"
#include "genibus/crc.h"
#include "genibus/interface.h"

/*
** Start-delimiters.
*/
#define GB_SD_REPLY     ((uint8)0x24)
#define GB_SD_MESSAGE   ((uint8)0x26)
#define GB_SD_REQUEST   ((uint8)0x27)


typedef enum tagDl_State {
    DL_IDLE,
    DL_SENDING,
    DL_RECEIVING
} Dl_State;


typedef enum tagDl_Error {
    DL_ERROR_NONE,
    DL_ERROR_TIMEOUT,
    DL_ERROR_CHECKSUM
} Dl_Error;

typedef enum tagGb_Error {
    ERR_INVALID_CRC
} Gb_Error;

typedef void (*Dl_Callout)(uint8 * buffer, uint8 len);
typedef void (*Error_Callout)(Gb_Error error, uint8 * buffer, uint8 len);

typedef struct tagDatalinkLayerType {
    Interface * port;
    Dl_Callout dataLinkCallout;
    Error_Callout errorCallout;
    uint8 scratchBuffer[0xff];
    //Crc _crc;
    Dl_State state;
    uint8 frameLength;
    boolean checked;
    uint8 frameIdx;
} DatalinkLayerType;

void LinkLayer_Init(DatalinkLayerType * linkLayer);
void LinkLayer_Reset(DatalinkLayerType * linkLayer);
void LinkLayer_SetState(DatalinkLayerType * linkLayer, Dl_State state);
Dl_State LinkLayer_GetState(DatalinkLayerType * linkLayer);
void LinkLayer_Feed(DatalinkLayerType * linkLayer);
boolean LinkLayer_VerifyCRC(DatalinkLayerType * linkLayer);
void LinkLayer_SendPDU(DatalinkLayerType * linkLayer, uint8 sd, uint8 da, uint8 sa, uint8 const * data, uint8 len);
void LinkLayer_ConnectRequest(DatalinkLayerType * linkLayer, uint8 sa);

#if 0
class GB_Datalink {
public:
/* TODO: rename 'callout', add errorCallout, add checked. */
    inline uint8 const * const getBufferPointer(void) const { return (uint8 const * const )_scratchBuffer; };
    void connectRequest(uint8 sa);
    void sendPDU(uint8 sd, uint8 da, uint8 sa, uint8 const * data, uint8 len);
    void sendRaw(uint8 const * data, uint8 len);
    void write(uint8 ch);
private:
    genibus::Interface & _port;
    Dl_Callout _dataLinkCallout;
    Error_Callout _errorCallout;
    uint8 _scratchBuffer[0xff];
    Crc _crc;
    Dl_State _state;
    uint8 _frameLength;
    boolean _checked;
    uint8 _idx;
};
#endif

#if defined(__cplusplus)
}
#endif  /* __cplusplus */

#endif /* __GB_DATALINK */

