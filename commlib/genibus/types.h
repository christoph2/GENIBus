/*
 *  Grundfos GENIBus Library.
 *
 *  (C) 2007-2016 by Christoph Schueler <cpu12.gems@googlemail.com>
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

/* http://www.opengroup.org/onlinepubs/000095399/basedefs/sys/types.h.html */

#if !defined(__TYPES_H)
#define __TYPES_H

/* Types  */
typedef unsigned char   boolean;
typedef signed char     sint8_t;
typedef unsigned char   uint8_t;
typedef signed short    sint16_t;
typedef unsigned short  uint16_t;
typedef signed long     sint32_t;
typedef unsigned long   uint32_t;

typedef signed char     sint8_least_t;
typedef unsigned char   uint8_least_t;
typedef signed short    sint16_least_t;
typedef unsigned short  uint16_least_t;
typedef signed long     sint32_least_t;
typedef unsigned long   uint32_least_t;

#if !defined(TRUE)
    #define TRUE    ((boolean)1)
#endif

#if !defined(FALSE)
    #define FALSE   ((boolean)0)
#endif

#endif

#if !defined(NULL)
#define NULL        0

typedef float           float32;
typedef double          float64;
typedef void *          pvoid;
typedef unsigned int    SizeType;
typedef int             PtrDiffType;

#define ARRAY_SIZE(a)   (sizeof((a)) / sizeof((a[0])))
#define VOID_EXPRESSION()           ((void)0)

#if !defined(UNREFERENCED_PARAMETER)
#define UNREFERENCED_PARAMETER(p)   ((p) = (p))
#endif

#define MIN(a, b)                   (((a) > (b)) ? (b) : (a))
#define MAX(a, b)                   (((a) > (b)) ? (a) : (b))

#define BETWEEN(x, min, max)        (((x) >= (min)) && ((x) <= (max)))

#define ABS(i)                      (((i) < 0) ? ((i) * -1) : ((i)))

#define SWAP_INPLACE(a, b)  \
    _BEGIN_BLOCK            \
        (a)    = (a) ^ (b); \
    (b)        = (a) ^ (b); \
    (a)        = (a) ^ (b); \
    _END_BLOCK

#if !defined(LOBYTE)
#define LOBYTE(w)                   ((uint8)((uint16)((uint16)(w) & 0x00ffU)))
#endif

#if !defined(HIBYTE)
#define HIBYTE(w)                   ((uint8)((uint16)(((uint16)(w ) >> 8) & 0x00ffU)))
#endif

#if !defined(LOWORD)
#define LOWORD(dw)                  ((uint16)((uint32)((uint32)(dw) & 0xffffU)))
#endif

#if !defined(HIWORD)
#define HIWORD(dw)                  ((uint16)((uint32)(((uint32)(dw) >> 16) & 0xffffU)))
#endif

#define MAKEWORD(h, l)              ((((uint16)((h) & ((uint8)0xff))) <<  (uint16)8) | ((uint16)((l) & ((uint8)0xff))))
#define MAKEDWORD(h, l)             ((((uint32)((h) & ((uint16)0xffffu))) << (uint32)16) | ((uint32)((l) & ((uint16)0xffffu))))

#define INVERT_NIBBLE(b)            ((uint8)(((uint8) ~(b)) & ((uint8)0x0f)))

#define SIZEOF_ARRAY(arr)           (sizeof((arr)) / sizeof((arr[0])))
#define BEYOND_ARRAY(arr)           ((arr) + SIZE_OF_ARRAY((arr)))

#if !defined(_countof)
#define _countof(arr)               SIZEOF_ARRAY(arr)
#endif


#endif /* __TYPES_H */

