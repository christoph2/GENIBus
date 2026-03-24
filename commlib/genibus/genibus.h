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
#if !defined(__GENIBUS_H)
#define __GENIBUS_H

#if defined(__cplusplus)
extern "C"
{
#endif  /* __cplusplus */


#if defined(__has_include)
	#if __has_include("genibus/crc.h")
		#include "genibus/crc.h"
	#elif __has_include("Crc.h")
		#include "Crc.h"
	#endif

	#if __has_include("genibus/datalink.h")
		#include "genibus/datalink.h"
	#elif __has_include("GB_Datalink.h")
		#include "GB_Datalink.h"
	#endif

	/* `Pdu.h` is legacy and optional in the current commlib layout. */
	#if __has_include("Pdu.h")
		#include "Pdu.h"
	#endif
#else
	#include "genibus/crc.h"
	#include "genibus/datalink.h"
#endif


#if defined(__cplusplus)
}
#endif  /* __cplusplus */


#endif /* __GENIBUS_H */

