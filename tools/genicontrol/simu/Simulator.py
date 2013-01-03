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
## Some known-good telegrams from spec.
##

import array
import unittest
from genicontrol.crc import Crc, checkCrc

## DATA Req/Resp
DATA_REQ = (
    0x27,   ##  Start Delimiter
    0x1F,   ##  Length
    0x20,   ##  Destination Address
    0x04,   ##  Source Address
            ##
    0x02,   ##  Class 2: Measured Data
    0x1B,   ##  OS=0 (GET),  Length=27
    0x51,   ##  act_mode1 = ID 81
    0x52,   ##  act_mode2 = ID 82
    0x53,   ##  act_mode3 = ID 83
    0x2F,   ##  led_contr = ID 47
    0x30,   ##  ref_act = ID 48
    0x31,   ##  ref_inf = ID 49
    0x3D,   ##  ref_att_loc = ID 61
    0x3E,   ##  sys_ref = ID 62
    0x25,   ##  h = ID 37
    0x27,   ##  q = ID 39
    0x2C,   ##  h_max = ID 44
    0x2B,   ##  q_max = ID 43
    0x18,   ##  2hour_hi = ID 24
    0x19,   ##  2hour_lo = ID 25
    0x5A,   ##  contr_source = ID 90
    0x57,   ##  ref_steps = ID 87
    0x22,   ##  p = ID 34
    0x98,   ##  energy_hi = ID 152
    0x99,   ##  energy_lo = ID 153
    0x23,   ##  speed = ID 35
    0x61,   ##  curve_no_ref = ID 97
    0x9E,   ##  alarm_code = ID 158
    0x9F,   ##  alarm_log1 = ID 159
    0xA0,   ##  alarm_log2 = ID 160
    0xA1,   ##  alarm_log3 = ID 161
    0xA2,   ##  alarm_log4 = ID 162
    0xA3,   ##  alarm_log5 = ID 163
            ##
    0x4B,   ##  CRC high
    0x8D,   ##  CRC low
)


DATA_RESP = (
    0x24,   ##  Start Delimiter
    0x1F,   ##  Length
    0x04,   ##  Destination Address
    0x20,   ##  Source Address
            ##
    0x02,   ##  Class 2: Measured Data
    0x1B,   ##  Ack.=0 (OK),  Length=27
    0x10,   ##  value example of act_mode1
    0x00,   ##  value example of act_mode2
    0x00,   ##  value example of act_mode3
    0x01,   ##  value example of led_contr
    0xA5,   ##  value example of ref_act
    0xFE,   ##  value example of ref_inf
    0xFE,   ##  value example of ref_att_loc
    0x94,   ##  value example of sys_ref
    0x7B,   ##  value example of h
    0x23,   ##  value example of q
    0xCD,   ##  value example of h_max
    0xB4,   ##  value example of q_max
    0x0B,   ##  value example of 2hour_hi
    0x80,   ##  value example of 2hour_lo
    0x22,   ##  value example of contr_source
    0x13,   ##  value example of ref_steps
    0xE9,   ##  value example of p
    0x0C,   ##  value example of energy_cons_hi
    0xE7,   ##  value example of energy_cons_lo
    0xA5,   ##  value example of speed
    0x0E,   ##  value example of curve_no_ref
    0x00,   ##  value example of alarm_code
    0x20,   ##  value example of alarm_log1
    0x39,   ##  value example of alarm_log2
    0x30,   ##  value example of alarm_log3
    0x40,   ##  value example of alarm_log4
    0x00,   ##  value example of alarm_log5
            ##
    0x19,   ##  CRC high
    0x6D,   ##  CRC low
)

## INFO req/resp
INFO_REQ = (
    0x27,   ##  Start Delimiter
    0x09,   ##  Length
    0x20,   ##  Destination Address
    0x04,   ##  Source Address
            ##
    0x02,   ##  Class 2: Measured Data
    0xC5,   ##  OS=3 (INFO),  Length=5
    0x25,   ##  h = ID 37
    0x27,   ##  q = ID 39
    0x22,   ##  p = ID 34
    0x23,   ##  speed = ID 35
    0x98,   ##  energy_hi = ID 152
            ##
    0xFA,   ##  CRC high
    0xA9,   ##  CRC low
)

INFO_RESP = (
    0x24,   ##  Start Delimiter
    0x18,   ##  Length
    0x04,   ##  Destination Address
    0x20,   ##  Source Address
            ##
    0x02,   ##  Class 2: Measured Data
    0x14,   ##  Ack.=0 (OK),  Length=20
    0x82,   ##  h INFO Head
    0x19,   ##  h UNIT
    0x00,   ##  h ZERO
    0x0C,   ##  h RANGE
    0x82,   ##  q INFO Head
    0x17,   ##  q UNIT
    0x00,   ##  q ZERO
    0x20,   ##  q RANGE
    0x82,   ##  p INFO Head
    0x09,   ##  p UNIT
    0x00,   ##  p ZERO
    0x28,   ##  p RANGE
    0x82,   ##  speed INFO Head
    0x13,   ##  speed UNIT
    0x00,   ##  speed ZERO
    0x24,   ##  speed RANGE
    0x82,   ##  energy_hi INFO Head
    0x2F,   ##  energy_hi UNIT
    0x00,   ##  energy_hi ZERO
    0xFE,   ##  energy_hi RANGE
            ##
    0xD9,   ##  CRC high
    0xBF,   ##  CRC low
)


## Refs req/resp
REF_REQ = (
    0x27,   ##  Start Delimiter
    0x09,   ##  Length
    0x20,   ##  Destination Address
    0x04,   ##  Source Address
            ##
    0x03,   ##  Class 3: Commands
    0x81,   ##  OS=2 (SET),  Length=1
    0x06,   ##  START = ID 6
    0x05,   ##  Class 5: Reference Values
    0x82,   ##  OS=2 (SET),  Length=2
    0x01,   ##  ref_rem = ID 1
    0xA5,   ##  ref_rem value example 65%
            ##
    0x28,   ##  CRC high
    0xDF,   ##  CRC low
)

REF_RESP = (
    0x24,   ##  Start Delimiter
    0x06,   ##  Length
    0x04,   ##  Destination Address
    0x20,   ##  Source Address
            ##
    0x03,   ##  Class 3: Commands
    0x00,   ##  Ack.=0 (OK),  Length=0
    0x05,   ##  Class 5: Reference Values
    0x00,   ##  Ack.=0 (OK),  Length=0
            ##
    0xC5,   ##  CRC high
    0x28,   ##  CRC low
)

## Conf req/resp
CONF_REQ = (
    0x27,   ##  Start Delimiter
    0x0D,   ##  Length
    0x20,   ##  Destination Address
    0x04,   ##  Source Address
            ##
    0x03,   ##  Class 3: Commands
    0x83,   ##  OS=2 (SET),  Length=3
    0x06,   ##  CONST_PRESS = ID 6
    0x1C,   ##  INFLUENCE_E = ID 28
    0x1F,   ##  UNLOCK_KEYS = ID 31
    0x04,   ##  Class 4: Configuration Parameters
    0x84,   ##  OS=2 (SET),  Length=4
    0x01,   ##  min_curve_no = ID 74
    0x01,   ##  value example = 1 (min curve 2)
    0x2E,   ##  unit_addr = ID 46
    0x24,   ##  value example = 36 (No. 5)
            ##
    0x50,   ##  CRC high
    0x62,   ##  CRC low
)

CONF_RESP = (
    0x24,   ##  Start Delimiter
    0x06,   ##  Length
    0x04,   ##  Destination Address
    0x20,   ##  Source Address
            ##
    0x03,   ##  Class 3: Commands
    0x00,   ##  Ack.=0 (OK),  Length=0
    0x04,   ##  Class 4: Configuration Parameters
    0x00,   ##  Ack.=0 (OK),  Length=0
            ##
    0xF6,   ##  CRC high
    0x19,   ##  CRC low
)

ALL_TELEGRAMS = (DATA_REQ, DATA_RESP, INFO_REQ, INFO_RESP, REF_REQ, REF_RESP, CONF_REQ, CONF_RESP)

START_DELIMITER     = 0
LENGTH              = 1
DESTINATION_ADRESS  = 2
SOURCE_ADDRESS      = 3
PDU_START           = 4

def makeBuffer(arr):
    return buffer(array.array('B', arr))

def makeArray(buf):
    return tuple([ord(x) for x in str(buf)])

def dissectResponse(frame):
    buf = makeBuffer(frame)
    arr =  makeArray(buf)

    sd = arr[START_DELIMITER]
    length = arr[LENGTH]
    da = arr[DESTINATION_ADRESS]
    sa = arr[SOURCE_ADDRESS]

    assert(length == len(arr) - 4)
    assert(frame == arr)
    for idx in range(PDU_START, length + 2):
        pass

def makeWord(bh, bl):
    return (bh <<8) | bl


class TestCrc(unittest.TestCase):
    """
        Test if Crc works as expected.
    """
    @staticmethod
    def check(frame):
        return checkCrc(frame)

    @staticmethod
    def expectedCrc(frame):
        return makeWord(frame[-2], frame[-1])

    def testDataReq(self):
        self.assertEquals(self.check(DATA_REQ), self.expectedCrc(DATA_REQ))

    def testDataResp(self):
        self.assertEquals(self.check(DATA_RESP), self.expectedCrc(DATA_RESP))

    def testInfoReq(self):
        self.assertEquals(self.check(INFO_REQ), self.expectedCrc(INFO_REQ))

    def testInfoResp(self):
        self.assertEquals(self.check(INFO_RESP), self.expectedCrc(INFO_RESP))

    def testRefReq(self):
        self.assertEquals(self.check(REF_REQ), self.expectedCrc(REF_REQ))

    def testRefResp(self):
        self.assertEquals(self.check(REF_RESP), self.expectedCrc(REF_RESP))

    def testConfReq(self):
        self.assertEquals(self.check(CONF_REQ), self.expectedCrc(CONF_REQ))

    def testConfResp(self):
        self.assertEquals(self.check(CONF_RESP), self.expectedCrc(CONF_RESP))


def main():
    dissectResponse(DATA_RESP)

if __name__ == '__main__':
    unittest.main()
    main()

