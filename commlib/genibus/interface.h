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


#if !defined(__INTERFACE_H)
#define __INTERFACE_H

namespace genibus {

#include <stdint.h>

class Interface {
public:
    Interface();
    virtual ~Interface();
    virtual uint8_t getLen(void) const = 0;
    virtual uint8_t write(uint8_t const * const buf, uint16_t len) = 0;
    virtual uint8_t write(uint8_t val) const = 0;
    virtual uint16_t available(void) const = 0;
    virtual int16_t read(void) const = 0;
};

} /// END namespace genibus.

#endif /* __INTERFACE_H */

