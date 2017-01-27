/*
 *  Grundfos GENIBus Library.
 *
 * (C) 2007-2016 by Christoph Schueler <github.com/Christoph2,
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

#ifndef __PORT_TIMER_H
#define __PORT_TIMER_H

#include "Wildfire_Config.h"
#include "knx_timer.h"

typedef struct tagPort_Timer_ConfigType {
    KnxTmr_TickHandlerType tickHandler;
    uint16_t tickResolution;
} Port_Timer_ConfigType;


#endif /* __PORT_TIMER_H*/

