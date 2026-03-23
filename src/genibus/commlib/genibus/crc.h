/*
 *  Grundfos GENIBus Library.
 *
 * (C) 2007-2017 by Christoph Schueler <github.com/Christoph2,
 *                                      cpu12.gems@googlemail.com>
 *
 * All Rights Reserved
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 *
 */
#if !defined(__CRC_H)
#define __CRC_H


#if defined(__cplusplus)
extern "C"
{
#endif  /* __cplusplus */


#include "genibus/types.h"

uint16 Crc_CalculateCRC16(uint8 const * Crc_DataPtr, uint16 Crc_Length, uint16 Crc_StartValue16);


#if 0
class Crc {
public:
  Crc(uint16 data = 0xffffu);
  void init(uint16 data);
  void update(uint8 data);
  uint16 get(void);
private:
  uint16 _accum;
};
#endif


#if defined(__cplusplus)
}
#endif  /* __cplusplus */

#endif /* __CRC_H */

