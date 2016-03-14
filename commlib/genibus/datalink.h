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


namespace genibus {

using namespace std;

#include "genibus/crc.h"
#include "genibus/interface.h"
#include <stdint.h>

/*
** Start-delimiters.
*/
#define GB_SD_REPLY     ((std::uint8_t)0x24)
#define GB_SD_MESSAGE   ((std::uint8_t)0x26)
#define GB_SD_REQUEST   ((std::uint8_t)0x27)


typedef enum tagDl_State {
    DL_IDLE,
    DL_SENDING,
    DL_RECEIVING
} Dl_State;


typedef enum tagGb_Error {
    ERR_INVALID_CRC
} Gb_Error;


typedef void (*Dl_Callout)(std::uint8_t * buffer, std::uint8_t len);
typedef void (*Error_Callout)(Gb_Error error, std::uint8_t * buffer, std::uint8_t len);

class GB_Datalink {
public:
/* TODO: rename 'callout', add errorCallout, add checked. */
    GB_Datalink(Interface & port, Dl_Callout dataLinkCallout = NULL, Error_Callout errorCallout = NULL, boolean checked = FALSE) :
        _port(port), _crc(0xffffu), _state(DL_IDLE), _dataLinkCallout(dataLinkCallout), _errorCallout(errorCallout),
        _checked(checked), _frameLength(0), _idx(0)
        { _port.begin(9600); };
    void reset(void);
    void feed(void);
    inline std::uint8_t const * const getBufferPointer(void) const { return (std::uint8_t const * const )_scratchBuffer; };
    inline Dl_State getState(void) const { return _state; };
    inline void setState(Dl_State state) { _state = state; };
    void connectRequest(std::uint8_t sa);
    void sendPDU(std::uint8_t sd, std::uint8_t da, std::uint8_t sa, std::uint8_t const * data, std::uint8_t len);
    void sendRaw(std::uint8_t const * data, std::uint8_t len);
    void write(std::uint8_t ch);
protected:
    std::uint16_t calculateCRC(std::uint8_t leftBound, std::uint8_t rightBound);
    bool verifyCRC(std::uint8_t leftBound, std::uint8_t rightBound);
private:
    Interface & _port;
    Dl_Callout _dataLinkCallout;
    Error_Callout _errorCallout;
    std::uint8_t _scratchBuffer[0xff];
    Crc _crc;
    Dl_State _state;
    std::uint8_t _frameLength;
    boolean _checked;
    std::uint8_t _idx;
};

}   // END namespace genibus.

#endif /* __GB_DATALINK */

