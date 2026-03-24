/*
 *  Grundfos GENIBus Library.
 *
 *  (C) 2007-2012 by Christoph Schueler <cpu12.gems@googlemail.com>
 *
 *   All Rights Reserved
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 */

#if !defined(__TYPES_H)
#define __TYPES_H

#if defined(__cplusplus)
#include <cstddef>
#include <cstdint>
extern "C" {
#else
#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>
#endif

typedef bool boolean;

typedef int8_t sint8;
typedef uint8_t uint8;
typedef int16_t sint16;
typedef uint16_t uint16;
typedef int32_t sint32;
typedef uint32_t uint32;

typedef int_least8_t sint8_least;
typedef uint_least8_t uint8_least;
typedef int_least16_t sint16_least;
typedef uint_least16_t uint16_least;
typedef int_least32_t sint32_least;
typedef uint_least32_t uint32_least;

#if !defined(TRUE)
#define TRUE ((boolean)true)
#endif

#if !defined(FALSE)
#define FALSE ((boolean)false)
#endif

typedef float float32;
typedef double float64;
typedef void *pvoid;
typedef unsigned int SizeType;
typedef int PtrDiffType;

#define ARRAY_SIZE(a) (sizeof((a)) / sizeof((a)[0]))
#define VOID_EXPRESSION() ((void)0)

#if !defined(UNREFERENCED_PARAMETER)
#define UNREFERENCED_PARAMETER(p) ((p) = (p))
#endif

#define MIN(a, b) (((a) > (b)) ? (b) : (a))
#define MAX(a, b) (((a) > (b)) ? (a) : (b))
#define BETWEEN(x, min, max) (((x) >= (min)) && ((x) <= (max)))
#define ABS(i) (((i) < 0) ? ((i) * -1) : (i))

#if !defined(LOBYTE)
#define LOBYTE(w) ((uint8)((uint16)((uint16)(w) & 0x00ffU)))
#endif

#if !defined(HIBYTE)
#define HIBYTE(w) ((uint8)((uint16)(((uint16)(w) >> 8) & 0x00ffU)))
#endif

#if !defined(LOWORD)
#define LOWORD(dw) ((uint16)((uint32)((uint32)(dw) & 0xffffU)))
#endif

#if !defined(HIWORD)
#define HIWORD(dw) ((uint16)((uint32)(((uint32)(dw) >> 16) & 0xffffU)))
#endif

#define MAKEWORD(h, l) ((((uint16)((h) & ((uint8)0xff))) << (uint16)8) | ((uint16)((l) & ((uint8)0xff))))
#define MAKEDWORD(h, l) ((((uint32)((h) & ((uint16)0xffffu))) << (uint32)16) | ((uint32)((l) & ((uint16)0xffffu))))
#define INVERT_NIBBLE(b) ((uint8)(((uint8) ~(b)) & ((uint8)0x0f)))

#define SIZEOF_ARRAY(arr) (sizeof((arr)) / sizeof((arr)[0]))
#define BEYOND_ARRAY(arr) ((arr) + SIZEOF_ARRAY((arr)))

#if !defined(_countof)
#define _countof(arr) SIZEOF_ARRAY(arr)
#endif

#if defined(__cplusplus)
}
#endif

#endif /* __TYPES_H */
