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
from collections import namedtuple
import logging
import unittest
from genicontrol.crc import checkCrc, calcuteCrc
from genicontrol.defs import Info, Item
import genicontrol.utils as utils
import genicontrol.apdu as apdu
import genicontrol.defs as defs
from genicontrol.utils import dumpHex
import genicontrol.dataitems as dataitems
from genicontrol.dissect import dissectResponse

logger = logging.getLogger("genicontrol")


## Connect Req/Resp
CONNECT_REQ = (
    0x27,   ##  Start Delimiter
    0x0e,   ##  Length
    0xfe,   ##  Destination Address
    0x01,   ##  Source Address
            ##
    0x00,   ##  Class 0: Protocol Data
    0x02,   ##  OS=0 (GET), Length=2
    0x02,   ##  df_buf_len
    0x03,   ##  unit_bus_mode
    0x04,   ##  Class 4: Configuration Data
    0x02,   ##  OS=0 (GET), Length=2
    0x2e,   ##  unit_addr
    0x2f,   ##  group_addr
    0x02,   ##  Class 2: Measured Data
    0x02,   ##  OS=0 (GET), Length=2
    0x94,   ##  unit_family
    0x95,   ##  unit_type
            ##
    0xa2,   ##  CRC high
    0xaa    ##  CRC low
)

CONNECT_RESP = (
    0x24,   ##  Start Delimiter
    0x0e,   ##  Length
    0x01,   ##  Destination Address
    0x20,   ##  Source Address
            ##
    0x00,   ##  Class 0: Protocol Data
    0x02,   ##  OS=0 (GET), Length=2
    0x46,   ##  df_buf_len
    0x0e,   ##  unit_bus_mode
    0x04,   ##  Class 4: Configuration Data
    0x02,   ##  Ack=0, Length=2
    0x20,   ##  unit_addr
    0xf7,   ##  group_addr
    0x02,   ##  Class 2: Measured Data
    0x02,   ##  Ack=0, Length=2
    0x03,   ##  unit_family
    0x01,   ##  unit_type
            ##
    0x00,   ##  CRC high
    0x04    ##  CRC low
)

## DATA Req/Resp
DATA_REQ = (
    0x27,   ##  Start Delimiter
    0x1E,   ##  Length
    0x20,   ##  Destination Address
    0x04,   ##  Source Address
            ##
    0x02,   ##  Class 2: Measured Data
    0x1A,   ##  OS=0 (GET),  Length=26
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
    0x18,   ##  t_2hour_hi = ID 24
    0x19,   ##  t_2hour_lo = ID 25
    0x5A,   ##  contr_source = ID 90
#    0x57,   ##  ref_steps = ID 87
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

    0x11,#0x4B,   ##  CRC high
    0x76#0x8D,   ##  CRC low
)


DATA_RESP = (
    0x24,   ##  Start Delimiter
    0x1E,   ##  Length
    0x04,   ##  Destination Address
    0x20,   ##  Source Address
            ##
    0x02,   ##  Class 2: Measured Data
    0x1A,   ##  Ack.=0 (OK),  Length=26
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
#    0x13,   ##  value example of ref_steps
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

    0xec, #0x19,   ##  CRC high
    0x8b#0x6D,   ##  CRC low
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

ALL_TELEGRAMS = (CONNECT_REQ, CONNECT_RESP, DATA_REQ, DATA_RESP, INFO_REQ, INFO_RESP, REF_REQ, REF_RESP, CONF_REQ, CONF_RESP)

class TestCrc(unittest.TestCase):
    """
        Test if Crc works as expected.
    """
    @staticmethod
    def check(frame):
        return checkCrc(frame)

    @staticmethod
    def expectedCrc(frame):
        return utils.makeWord(frame[defs.CRC_HIGH], frame[defs.CRC_LOW])

    def testConnReq(self):
        self.assertEquals(self.check(CONNECT_REQ), self.expectedCrc(CONNECT_REQ))

    def testConnResp(self):
        self.assertEquals(self.check(CONNECT_RESP), self.expectedCrc(CONNECT_RESP))

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



dataReqValues = (
    "act_mode1", "act_mode2", "act_mode3", "led_contr", "ref_act", "ref_inf", "ref_att_loc", "sys_ref", "h", "q",
    "h_max", "q_max", "t_2hour_hi", "t_2hour_lo", "contr_source", "p", "energy_hi", "energy_lo", "speed",
    "curve_no_ref", "alarm_code", "alarm_log_1", "alarm_log_2", "alarm_log_3", "alarm_log_4", "alarm_log_5"
)

infoReqValues = (
    "h", "q", "p", "speed", "energy_hi"
)

refSetValues = (
    ("ref_rem", 0xa5, ),
)

commandSetValues = (
    "RESET_ALARM", "REMOTE", "START", "PROP_PRESS"
)

DATA_POOL = { # This dictionary is used to 'simulate' communication.
    defs.ADPUClass.PROTOCOL_DATA: {
        Item(u"df_buf_len", 0x46, None),
        Item(u"unit_bus_mode", 0x0e, None)
    },
    defs.ADPUClass.MEASURERED_DATA: {
        Item(u"i_mo", 0x7a, Info(0x82, 0x3e, 0x00, 0x39)),
        #Item("t_mo", 0x42, Info(0x82, 0x15, 0x00, 0x64)),
        #Item("p_hi", 0x39, Info(0x82, 0x09, 0x00, 0xfa)),
        #Item("p_lo", 0x80, None),
        #Item("i_rst_max_stop", 0xc8, Info(0x81, None, None, None)),
        #Item("t_mo_stop", 0xb5, None),
        Item(u"act_mode1", 0x10,     Info(0x81, None, None, None)),
        Item(u"act_mode2", 0x00,     Info(0x81, None, None, None)),
        Item(u"act_mode3", 0x00,     Info(0x81, None, None, None)),
        Item(u"led_contr", 0x01,     Info(0x81, None, None, None)),
        Item(u"ref_act", 0xa5,       Info(0x81, None, None, None)),
        Item(u"ref_inf", 0xfe,       Info(0x81, None, None, None)),
        Item(u"ref_att_loc", 0xfe,   Info(0x81, None, None, None)),
        Item(u"ref_loc", 0x80,       Info(0x81, None, None, None)),
        Item(u"i_dc", 0x80,         Info(0x81, None, None, None)),
        Item(u"q_kn1", 0x80,       Info(0x81, None, None, None)),
        Item(u"stop_alarm1_bak", 0x80,  Info(0x81, None, None, None)),
        Item(u"stop_alarm2_bak", 0x80,  Info(0x81, None, None, None)),
        Item(u"stop_alarm3_bak", 0x80,  Info(0x81, None, None, None)),
        Item(u"ind_alarm_bak", 0x80,       Info(0x81, None, None, None)),
        Item(u"alarm_code_disp", 0x80,       Info(0x81, None, None, None)),
        Item(u"unit_version", 0x80,       Info(0x81, None, None, None)),
        Item(u"surv_alarm1_bak", 0x80,       Info(0x81, None, None, None)),
        Item(u"surv_alarm2_bak", 0x80,       Info(0x81, None, None, None)),
        Item(u"surv_alarm3_bak", 0x80,       Info(0x81, None, None, None)),
        Item(u"loc_setup1", 0x80,       Info(0x81, None, None, None)),
        Item(u"rem_setup1", 0x80,       Info(0x81, None, None, None)),
        Item(u"stop_alarm1", 0x80,       Info(0x81, None, None, None)),
        Item(u"stop_alarm2", 0x80,       Info(0x81, None, None, None)),
        Item(u"stop_alarm3", 0x80,       Info(0x81, None, None, None)),
        Item(u"t_w", 0x80,       Info(0x81, None, None, None)),
        Item(u"ind_alarm", 0x80,       Info(0x81, None, None, None)),
        Item(u"contr_ref", 0x80,       Info(0x81, None, None, None)),
        Item(u"t_m", 0x80,       Info(0x81, None, None, None)),
        Item(u"i_line", 0x80,       Info(0x81, None, None, None)),
        Item(u"surv_alarm1", 0x80,       Info(0x81, None, None, None)),
        Item(u"surv_alarm2", 0x80,       Info(0x81, None, None, None)),
        Item(u"surv_alarm3", 0x80,       Info(0x81, None, None, None)),
        Item(u"t_e", 0x80,       Info(0x81, None, None, None)),
        Item(u"start_alarm1_bak", 0x80,       Info(0x81, None, None, None)),
        Item(u"start_alarm2_bak", 0x80,       Info(0x81, None, None, None)),
        Item(u"start_alarm3_bak", 0x80,       Info(0x81, None, None, None)),
        Item(u"v_dc", 0x80,       Info(0x81, None, None, None)),
        Item(u"start_alarm1", 0x80,       Info(0x81, None, None, None)),
        Item(u"start_alarm2", 0x80,       Info(0x81, None, None, None)),
        Item(u"start_alarm3", 0x80,       Info(0x81, None, None, None)),
        Item(u"twin_pump_mode", 0x80,       Info(0x81, None, None, None)),
        Item(u"extern_inputs", 0x80,       Info(0x81, None, None, None)),
        Item(u"qsd_alarm1", 0x80,       Info(0x81, None, None, None)),
        Item(u"qsd_alarm2", 0x80,       Info(0x81, None, None, None)),
        Item(u"qsd_alarm3", 0x80,       Info(0x81, None, None, None)),
        Item(u"p_max", 0x80,       Info(0x81, None, None, None)),

        Item(u"qsd_alarm1_bak", 0x80,       Info(0x81, None, None, None)),
        Item(u"qsd_alarm2_bak", 0x80,       Info(0x81, None, None, None)),
        Item(u"qsd_alarm3_bak", 0x80,       Info(0x81, None, None, None)),
        Item(u"sys_ref", 0x94,       Info(0x81, None, None, None)),
        Item(u"h", 0x7b,             Info(0x82, 0x19, 0x00, 0x0c)),
        Item(u"q", 0x23,             Info(0x82, 0x17, 0x00, 0x20)),
        Item(u"h_max", 0xcd,         Info(0x81, None, None, None)),
        Item(u"q_max", 0xb4,         Info(0x81, None, None, None)),
        Item(u"f_act", 0xa4,         Info(0x81, None, None, None)),
        Item(u"t_2hour_hi", 0x0b,    Info(0x81, None, None, None)),
        Item(u"t_2hour_lo", 0x80,    Info(0x81, None, None, None)),
        Item(u"contr_source", 0x22,  Info(0x81, None, None, None)),
        Item(u"p", 0xe9,             Info(0x82, 0x09, 0x00, 0x28)),
        Item(u"energy_hi", 0x0c,     Info(0x82, 0x2f, 0x00, 0xfe)),
        Item(u"energy_lo", 0xe7,     Info(0x81, None, None, None)),
        Item(u"speed", 0xa5,         Info(0x82, 0x13, 0x00, 0x24)),
        Item(u"curve_no_ref", 0x0e,  Info(0x81, None, None, None)),
        Item(u"alarm_code", 0x00,    Info(0x81, None, None, None)),
        Item(u"alarm_log_1", 0x20,   Info(0x81, None, None, None)),
        Item(u"alarm_log_2", 0x39,   Info(0x81, None, None, None)),
        Item(u"alarm_log_3", 0x30,   Info(0x81, None, None, None)),
        Item(u"alarm_log_4", 0x40,   Info(0x81, None, None, None)),
        Item(u"alarm_log_5", 0x00,   Info(0x81, None, None, None)),
        Item(u"unit_family", 0x03,   Info(0x81, None, None, None)),
        Item(u"unit_type", 0x01,     Info(0x81, None, None, None)),
    },
    defs.ADPUClass.COMMANDS: {
        Item(u"RESET",           None,   Info(None, None, None, None)),
        Item(u"RESET_ALARM",     None,   Info(None, None, None, None)),
        Item(u"USER_BOOT",       None,   Info(None, None, None, None)),
        Item(u"STOP",            None,   Info(None, None, None, None)),
        Item(u"START",           None,   Info(None, None, None, None)),
        Item(u"REMOTE",          None,   Info(None, None, None, None)),
        Item(u"LOCAL",           None,   Info(None, None, None, None)),
        Item(u"RUN",             None,   Info(None, None, None, None)),
        Item(u"PROGRAM",         None,   Info(None, None, None, None)),
        Item(u"CONST_FREQ",      None,   Info(None, None, None, None)),
        Item(u"PROP_PRESS",      None,   Info(None, None, None, None)),
        Item(u"CONST_PRESS",     None,   Info(None, None, None, None)),
        Item(u"MIN",             None,   Info(None, None, None, None)),
        Item(u"MAX",             None,   Info(None, None, None, None)),
        Item(u"INFLUENCE_E",     None,   Info(None, None, None, None)),
        Item(u"INFLUENCE_D",     None,   Info(None, None, None, None)),
        Item(u"LOCK_KEYS",       None,   Info(None, None, None, None)),
        Item(u"UNLOCK_KEYS",     None,   Info(None, None, None, None)),
        Item(u"REF_UP",          None,   Info(None, None, None, None)),
        Item(u"REF_DOWN",        None,   Info(None, None, None, None)),
        Item(u"RESET_HIST",      None,   Info(None, None, None, None)),
        Item(u"RESET_ALARM_LOG", None,   Info(None, None, None, None)),
        Item(u"AUTOMATIC",       None,   Info(None, None, None, None)),
        Item(u"TWIN_MODE_SPARE", None,   Info(None, None, None, None)),
        Item(u"TWIN_MODE_ALT",   None,   Info(None, None, None, None)),
        Item(u"TWIN_MODE_SYNC",  None,   Info(None, None, None, None)),
        Item(u"NIGHT_REDUCT_E+", None,   Info(None, None, None, None)),
        Item(u"NIGHT_REDUCT_D+", None,   Info(None, None, None, None)),
    },
    defs.ADPUClass.CONFIGURATION_PARAMETERS: {
        Item(u"unit_addr",      0x20, Info(0x81, None, None, None)),
        Item(u"group_addr",     0xf7, Info(0x81, None, None, None)),
        Item(u"min_curve_no",      0x01, Info(0x81, None, None, None)),
        Item(u"h_const_ref_min",   0x01, Info(0x81, None, None, None)),
        Item(u"h_const_ref_max",   0xfe, Info(0x81, None, None, None)),
        Item(u"h_prop_ref_min",    0x01, Info(0x81, None, None, None)),
        Item(u"h_prop_ref_max",    0xfe, Info(0x81, None, None, None)),
        Item(u"ref_steps",         0x09, Info(0x81, None, None, None)),
    },
    defs.ADPUClass.REFERENCE_VALUES: {
        Item(u"ref_rem",        0x10, Info(0x81, None, None, None)),
        Item(u"ref_ir",         0x20, Info(0x81, None, None, None)),
        Item(u"ref_att_rem",    0x30, Info(0x81, None, None, None)),
    },
    defs.ADPUClass.ASCII_STRINGS: {},
}


def getParameterValue(name):
    return [p.value for p in DATA_POOL[defs.ADPUClass.CONFIGURATION_PARAMETERS] if p.name == name][0]


class TestDataPool(unittest.TestCase):
    def testCorrectnessOfKeys(self):
        for klass, values in DATA_POOL.items():
            di = dataitems.DATAITEMS_FOR_CLASS[klass]
            for value in values:
                if not value.name in di:
                    raise KeyError('invalid datapoint "%s"' % value.name)


def createResponse(request):
    """The actual 'simulation' function.
    """
    result = []
    length = 2
    pdus = []
    #klasses = []
    for a in request.APDUs:
        klass = a.klass
        ack = a.ack
        data = a.data
        dataItemsByName = dict([(a, (b, c)) for a, b ,c in DATA_POOL[klass]])

        if ack not in defs.CLASS_CAPABILITIES[klass]:
            raise defs.IllegalOperationError("%s-Operation not supported." % defs.operationToString(ack))
        dataItemsById = dict([(v[2], (k, v[3], v[4])) for k, v in dataitems.DATAITEMS_FOR_CLASS[klass].items()])
        apduLength = 0
        length += 2
        pdu = []
        if ack == defs.OS_SET:
            pass # Ack = OK, Length = 0 is inherently generated!
        else:
            for item in data:
                name, acess, _ = dataItemsById[item]
                #print "KLASS: %s NAME: %s " % (klass, name)
                value, info = dataItemsByName[name]
                if ack == defs.OS_GET:
                    apduLength += 1 # Currently only 8-bit data values.
                    value = 0xff if value is None else value
                    pdu.append(value)
                elif ack == defs.OS_INFO:
                    sif = info.head & 0b11
                    pdu.append(info.head)
                    if sif in (0, 1):
                        apduLength += 1 # Unscaled value, i.e. no info scale field.
                    else:
                        apduLength += 4
                        pdu.append(info.unit)
                        pdu.append(info.zero)
                        pdu.append(info.range)
        pdus.append((klass, apduLength, pdu, ))
        length += apduLength
    if request.da == defs.CONNECTION_REQ_ADDR:
        da = getParameterValue('unit_addr') # Handle connection address.
    else:
        da = request.da
    result.extend([defs.SD_DATA_REPLY, length, request.sa, da])
    for pdu in pdus:
        klass, apduLength, pdu = pdu
        result.append(klass)
        result.append(apduLength & 0x3f)
        result.extend(pdu)
    crc = calcuteCrc(result)
    result.extend((utils.hiByte(crc), utils.loByte(crc), ))
    return bytearray(result)


import genicontrol.conversion as conversion
import genicontrol.units as units


ValueType = namedtuple('ValueType', 'name unit value')
AckType = namedtuple('AckType', 'klass ack')


from genicontrol.connection import ConnectionIF

class SimulationServer(ConnectionIF):
    DRIVER = 'Simulator'

    def __init__(self, *args, **kwargs):
        self._request = None
        self._response = None
        self.connected = False

    def connect(self):
        self.connected = True
        return True

    def disconnect(self):
        self.connected = False

    def close(self):
        self.connected = False

    def write(self, req):
        if self.connected:
             resp = createResponse(dissectResponse(req))
             self._response = resp

    def read(self, numBytes):
        if self.connected:
             resp = array.array('B', self._response)
             self._response = None
             return resp
    @property
    def displayName(self):
        return "Simulator"


def testResponse(telegram, datapoints, valueInterpretation):
    res = createResponse(dissectResponse(telegram))
    dr = dissectResponse(res)
    print rawInterpreteResponse(dr, datapoints, valueInterpretation)
    print


def printTuple(data, name):
    print "%s = (" % name
    for d in data:
        print "     0x%02x," % d

    print ")"

def createStaticTelegrams():
    """
    Create telegrams for TestClient.
    """
    # First transform dictionary.
    dd= dict.fromkeys(set([x.klass for x in dataitems.DATAITEMS if not (x.klass in (0, 3, 7))]))
    for key in dd.keys():
        dd[key] = dict()
    for item in dataitems.DATAITEMS:
        name, klass, _id, _, _ = item
        if klass in (0, 3, 7):
            continue
        dd[klass][name] = _id
    for klass, items in dd.items():
        print klass
        # [it[i:i+n] for i in range(0, len(it), n)]
        items = items.items()
        if len(items) > 15:
            slices = [items [i : i + 15] for i in range(0, len(items), 15)]
        else:
            slices = [items]
        for idx, slice in enumerate(slices):
            slice = [n for n,i in slice]
            if klass == defs.ADPUClass.MEASURERED_DATA:
                telegram = apdu.createGetInfoPDU(apdu.Header(defs.SD_DATA_REQUEST, 0x20, 0x04), measurements = slice)
            elif klass == defs.ADPUClass.REFERENCE_VALUES:
                telegram = apdu.createGetInfoPDU(apdu.Header(defs.SD_DATA_REQUEST, 0x20, 0x04), references = slice)
            elif klass == defs.ADPUClass.CONFIGURATION_PARAMETERS:
                telegram = apdu.createGetInfoPDU(apdu.Header(defs.SD_DATA_REQUEST, 0x20, 0x04), parameter = slice)
            printTuple(telegram, "INFO_REQUEST%u" % idx)

import sys


class MyList(list):
    type = None


def rawInterpreteResponse(response, datapoints, valueInterpretation):
    result = MyList()
    for apdu in response.APDUs:
        if valueInterpretation == defs.OS_GET:
            dataItemsByName = dict([(a, (b, c)) for a, b ,c in DATA_POOL[apdu.klass]])
            for name, value in zip(datapoints, apdu.data):
                _, (head, unit, zero, range) = dataItemsByName[name]
                if head == 0x82:
                    unitInfo = units.UnitTable[unit]
                    result.append(ValueType(name, unitInfo.unit, conversion.convertForward8(value, zero, range, unitInfo.factor)))
        elif valueInterpretation == defs.OS_INFO:
            idx = 0
            values = []
            for datapoint in datapoints:
                data = apdu.data[idx]
                sif = data & 0b11
                if sif in (0, 1):
                    result.append(Info(data, None, None, None))
                    idx += 1    # No scaling information.
                else:
                    result.append(Info(data, apdu.data[idx + 1], apdu.data[idx + 2], apdu.data[idx + 3]))
                    idx += 4
        elif valueInterpretation == defs.OS_SET:
            result.append(AckType(apdu.klass, apdu.ack >> 6))
    result.type = valueInterpretation
    return result

def main():
    createStaticTelegrams()
    telegram = apdu.createGetValuesPDU(apdu.Header(defs.SD_DATA_REQUEST, 0x20, 0x04), measurements = dataReqValues)
    testResponse(telegram, dataReqValues, defs.OS_GET)

    telegram = apdu.createGetInfoPDU(apdu.Header(defs.SD_DATA_REQUEST, 0x20, 0x04), measurements = infoReqValues)
    testResponse(telegram, infoReqValues, defs.OS_INFO)

    telegram = apdu.createSetCommandsPDU(apdu.Header(defs.SD_DATA_REQUEST, 0x20, 0x04), commands = commandSetValues)
    testResponse(telegram, commandSetValues, defs.OS_SET)


if __name__ == '__main__':
    main()
    unittest.main()

