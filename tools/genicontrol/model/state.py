#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2013 by Christoph Schueler <github.com/Christoph2,
##                                      cpu12.gems@googlemail.com>
##
##  All Rights Reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License along
## with this program; if not, write to the Free Software Foundation, Inc.,
## 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
##
##

##
## Current (actual) state of the pump.
## Mainly used for command feedback.
##

import threading


USER_MODE_START                     = 0b000
USER_MODE_STOP                      = 0b001
USER_MODE_MIN                       = 0b010
USER_MODE_MAX                       = 0b011

CONTROL_MODE_CONSTANT_PRESSURE      = 0b000 << 3
CONTROL_MODE_PROPORTIONAL_PRESSURE  = 0b001 << 3
CONTROL_MODE_CONSTANT_FREQUENCY     = 0b010 << 3
CONTROL_MODE_AUTOADAPT_SETPOINT     = 0b101 << 3

NIGHT_REDUCTION_DISABLED            = 0 << 6
NIGHT_REDUCTION_ENABLED             = 1 << 6

TEMPERATURE_INFLUENCE_DISABLED      = 0
TEMPERATURE_INFLUENCE_ENABLED       = 1

BUTTONS_ON_PUMP_ENABLED             = 0 << 5
BUTTONS_ON_PUMP_DISABLED            = 1 << 5

MINIMUM_CURVE_1                     = 0 << 6
MINIMUM_CURVE_2                     = 1 << 6

SYSTEM_MODE_NORMAL                  = 0b000
SYSTEM_MODE_SURVIVE                 = 0b011
SYSTEM_MODE_ALARM_STANDBY           = 0b100

PENDING_ALARM_TRUE                  = 0b1 << 3
PENDING_ALARM_FALSE                 = 0b0 << 3

SOURCE_MODE_REMOTE                  = 0 << 4
SOURCE_MODE_LOCAL                   = 1 << 4

TWIN_PUMP_MODE_SINGLE_PUMP                  = 0
TWIN_PUMP_MODE_TWIN_PUMP_SLAVE              = 1
TWIN_PUMP_MODE_TWIN_PUMP_MASTER_SPARE       = 2
TWIN_PUMP_MODE_TWIN_PUMP_MASTER_SYNCHRONOUS = 3
TWIN_PUMP_MODE_TWIN_PUMP_MASTER_ALTERNATING = 4

LED_GREEN_OFF                       = 0
LED_GREEN_ON                        = 1
LED_GREEN_BLINKING                  = 2

LED_RED_OFF                         = 0 << 2
LED_RED_ON                          = 1 << 2
LED_RED_BLINKING                    = 2 << 2


class PumpState(object):
    _lock = threading.Lock()

    def __new__(cls):
        try:
            cls._lock.acquire()
            if not hasattr(cls, '_instance'):
                cls._instance = super(cls.__class__, cls).__new__(cls)
        finally:
            cls._lock.release()
        return cls._instance

    def __init__(self):
        self.userMode = None
        self.controlMode = None
        self.nightReduction = None
        self.temperatureInfuence = None
        self.buttonsOnPump = None
        self.minimumCurve = None
        self.systemMode = None
        self.pendingAlarm = None
        self.sourceMode = None
        self.twinPumpMode = None
        self.ledState = None

