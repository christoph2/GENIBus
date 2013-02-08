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


#include "Crc.h"
#include "HardwareSerial.h"

#if !defined(__GB_DATALINK)
#define __GB_DATALINK

#if defined(__cplusplus)
extern "C"
{
#endif  /* __cplusplus */


typedef enum tagDl_State {
    DL_IDLE,
    DL_SENDING,
    DL_RECEIVING,
} Dl_State;


typedef void (*Dl_Callout)(uint8 * buffer, uint8 len);

class GB_Datalink {
public:
/* TODO: rename 'callout', add errorCallout, add checked. */
    GB_Datalink(HardwareSerial & port, Dl_Callout callout = NULL, boolean checked = FALSE) :
        _port(port), _crc(0xffffu), _state(DL_IDLE), _callout(callout), _checked(checked), _frameLength(0)
        { _port.begin(9600); };
    void feed(void);
    inline uint8 const * const getBufferPointer(void) const { return (uint8 const * const )_scratchBuffer; };
    inline Dl_State getState(void) const { return _state; };
    inline void setState(Dl_State state) { _state = state; };
    void connectRequest(uint8 sa);
    void sendPDU(uint8 sd, uint8 da, uint8 sa, uint8 const * data, uint8 len);
    void sendRaw(uint8 const * data, uint8 len);
    void write(uint8 ch);
protected:
    uint16 calculateCRC(uint8 leftBound, uint8 rightBound);
    bool verifyCRC(uint8 leftBound, uint8 rightBound);
private:
    HardwareSerial & _port;
    Dl_Callout _callout;
    uint8 _scratchBuffer[0xff];
    Crc _crc;
    Dl_State _state;
    uint8 _frameLength;
    boolean _checked;
};


#if defined(__cplusplus)
}
#endif  /* __cplusplus */

#endif /* __GB_DATALINK */

