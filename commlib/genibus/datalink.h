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

namespace genibus {

#include "genibus/crc.h"
#include "genibus/interface.h"
#include <stdint.h>

#if !defined(__GB_DATALINK)
#define __GB_DATALINK

#if defined(__cplusplus)
extern "C"
{
#endif  /* __cplusplus */

/*
** Start-delimiters.
*/
#define GB_SD_REPLY     ((uint8_t)0x24)
#define GB_SD_MESSAGE   ((uint8_t)0x26)
#define GB_SD_REQUEST   ((uint8_t)0x27)


typedef enum tagDl_State {
    DL_IDLE,
    DL_SENDING,
    DL_RECEIVING,
} Dl_State;


typedef enum tagGb_Error {
    ERR_INVALID_CRC
} Gb_Error;


typedef void (*Dl_Callout)(uint8_t * buffer, uint8_t len);
typedef void (*Error_Callout)(Gb_Error error, uint8_t * buffer, uint8_t len);

class GB_Datalink {
public:
/* TODO: rename 'callout', add errorCallout, add checked. */
    GB_Datalink(Interface & port, Dl_Callout dataLinkCallout = NULL, Error_Callout errorCallout = NULL, boolean checked = FALSE) :
        _port(port), _crc(0xffffu), _state(DL_IDLE), _dataLinkCallout(dataLinkCallout), _errorCallout(errorCallout),
        _checked(checked), _frameLength(0), _idx(0)
        { _port.begin(9600); };
    void reset(void);
    void feed(void);
    inline uint8_t const * const getBufferPointer(void) const { return (uint8_t const * const )_scratchBuffer; };
    inline Dl_State getState(void) const { return _state; };
    inline void setState(Dl_State state) { _state = state; };
    void connectRequest(uint8_t sa);
    void sendPDU(uint8_t sd, uint8_t da, uint8_t sa, uint8_t const * data, uint8_t len);
    void sendRaw(uint8_t const * data, uint8_t len);
    void write(uint8_t ch);
protected:
    uint16_t calculateCRC(uint8_t leftBound, uint8_t rightBound);
    bool verifyCRC(uint8_t leftBound, uint8_t rightBound);
private:
    Interface & _port;
    Dl_Callout _dataLinkCallout;
    Error_Callout _errorCallout;
    uint8_t _scratchBuffer[0xff];
    Crc _crc;
    Dl_State _state;
    uint8_t _frameLength;
    boolean _checked;
    uint8_t _idx;
};

}   // END namespace genibus.

#endif /* __GB_DATALINK */

