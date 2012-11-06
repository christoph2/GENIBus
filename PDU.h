/*
 *  Grundfos GENIBus Library.
 *
 *  (C) 2007-2012 by Christoph Schueler <github.com/Christoph2,
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

#if !defined(__PDU_H)
#define __PDU_H

#include "GENIBus.h"

#if defined(__cplusplus)
extern "C"
{
#endif  /* __cplusplus */


/*
** Start-delimiters.
*/
#define GB_SD_REPLY     ((uint8)0x24)
#define GB_SD_MESSAGE   ((uint8)0x26)
#define GB_SD_REQUEST   ((uint8)0x27)
	


#if defined(__cplusplus)
}
#endif  /* __cplusplus */

#endif /* __PDU_H */

