#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2014 by Christoph Schueler <github.com/Christoph2,
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

import array
from collections import namedtuple
import logging
#import unittest
#from genilib.crc import checkCrc, calcuteCrc
from genicontrol.defs import Info, Item
import genilib.utils as utils
import genicontrol.apdu as apdu
import genicontrol.defs as defs
from genilib.utils import dumpHex
import genicontrol.dataitems as dataitems
from genicontrol.dissect import dissectResponse

logger = logging.getLogger("GeniControl")


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
        Item(u"df_buf_len",         0x46, None),
        Item(u"unit_bus_mode",      0x4e, None)
    },
    defs.ADPUClass.MEASURERED_DATA: {
        Item(u"i_mo", 0x7a,          Info(0x80, None, None, None)),
        #Item("t_mo", 0x42, Info(0x82, 0x15, 0x00, 0x64)),
        #Item("p_hi", 0x39, Info(0x82, 0x09, 0x00, 0xfa)),
        #Item("p_lo", 0x80, None),
        #Item("i_rst_max_stop", 0xc8, Info(0x81, None, None, None)),
        #Item("t_mo_stop", 0xb5, None),

        Item(u"act_mode1", 0x08,         Info(0x81, None, None, None)),
        Item(u"act_mode2", 0x00,         Info(0x81, None, None, None)),
        Item(u"act_mode3", 0x10,         Info(0x81, None, None, None)),
        Item(u"led_contr", 0x01,         Info(0x81, None, None, None)),
        Item(u"ref_act", 0xa5,           Info(0x82, 0x19, 0x00, 0x0b)),
        Item(u"ref_inf", 0xfe,           Info(0x82, 0x1e, 0x00, 0x64)),
        Item(u"ref_att_loc", 0xfe,       Info(0x82, 0x1e, 0x00, 0x64)),
        Item(u"ref_loc", 0x80,           Info(0x80, None, None, None)),
        Item(u"i_dc", 0x80,              Info(0x82, 0x2a, 0x00, 0x06)),
        Item(u"q_kn1", 0x80,             Info(0x82, 0x17, 0x00, 0x0c)),
        Item(u"stop_alarm1_bak", 0x80,   Info(0x81, None, None, None)),
        Item(u"stop_alarm2_bak", 0x80,   Info(0x81, None, None, None)),
        Item(u"stop_alarm3_bak", 0x80,   Info(0x81, None, None, None)),
        Item(u"ind_alarm_bak", 0x81,     Info(0x81, None, None, None)),
        Item(u"alarm_code_disp", 0x80,   Info(0xa0, None, None, None)),
        Item(u"unit_version", 0x80,      Info(0x80, None, None, None)),
        Item(u"surv_alarm1_bak", 0x80,   Info(0x81, None, None, None)),
        Item(u"surv_alarm2_bak", 0x80,   Info(0x81, None, None, None)),
        Item(u"surv_alarm3_bak", 0x80,   Info(0x81, None, None, None)),
        Item(u"loc_setup1", 0x80,        Info(0x81, None, None, None)),
        Item(u"rem_setup1", 0x80,        Info(0x81, None, None, None)),
        Item(u"stop_alarm1", 0x80,       Info(0x81, None, None, None)),
        Item(u"stop_alarm2", 0x80,       Info(0x81, None, None, None)),
        Item(u"stop_alarm3", 0x80,       Info(0x81, None, None, None)),
        Item(u"t_w", 0x80,               Info(0x82, 0x15, 0x00, 0xfe)),
        Item(u"ind_alarm", 0x81,         Info(0x81, None, None, None)),
        Item(u"contr_ref", 0x80,         Info(0x80, None, None, None)),
        Item(u"t_m", 0x80,               Info(0x82, 0x15, 0x00, 0xfe)),
        Item(u"i_line", 0x80,            Info(0x80, None, None, None)),
        Item(u"surv_alarm1", 0x80,       Info(0x81, None, None, None)),
        Item(u"surv_alarm2", 0x80,       Info(0x81, None, None, None)),
        Item(u"surv_alarm3", 0x80,       Info(0x81, None, None, None)),
        Item(u"t_e", 0x80,               Info(0x80, None, None, None)),
        Item(u"start_alarm1_bak", 0x80,  Info(0x81, None, None, None)),
        Item(u"start_alarm2_bak", 0x80,  Info(0x81, None, None, None)),
        Item(u"start_alarm3_bak", 0x80,  Info(0x81, None, None, None)),
        Item(u"v_dc", 0x80,              Info(0x82, 0x05, 0x00, 0x51)),
        Item(u"start_alarm1", 0x80,      Info(0x81, None, None, None)),
        Item(u"start_alarm2", 0x80,      Info(0x81, None, None, None)),
        Item(u"start_alarm3", 0x80,      Info(0x81, None, None, None)),
        Item(u"twin_pump_mode", 0x80,    Info(0x81, None, None, None)),
        Item(u"extern_inputs", 0x80,     Info(0x81, None, None, None)),
        Item(u"qsd_alarm1", 0x80,        Info(0x81, None, None, None)),
        Item(u"qsd_alarm2", 0x80,        Info(0x81, None, None, None)),
        Item(u"qsd_alarm3", 0x80,        Info(0x81, None, None, None)),
        Item(u"p_max",      0x80,        Info(0x82, 0x09, 0x00, 0x03)),

        Item(u"qsd_alarm1_bak", 0x80,    Info(0x81, None, None, None)),
        Item(u"qsd_alarm2_bak", 0x80,    Info(0x81, None, None, None)),
        Item(u"qsd_alarm3_bak", 0x80,    Info(0x81, None, None, None)),
        Item(u"sys_ref", 0x94,           Info(0x82, 0x19, 0x00, 0x0b)),
        Item(u"h", 0x17,                 Info(0x82, 0x19, 0x00, 0x0b)),
        Item(u"q", 0x26,                 Info(0x82, 0x17, 0x00, 0x0c)),
        Item(u"h_max", 0xcd,             Info(0x82, 0x19, 0x00, 0x0b)),
        Item(u"q_max", 0xb4,             Info(0x82, 0x17, 0x00, 0x0c)),
        Item(u"f_act", 0x57,             Info(0x82, 0x26, 0x00, 0x47)),
        Item(u"t_2hour_hi", 0x00,        Info(0x82, 0x27, 0x00, 0x7f)),
        Item(u"t_2hour_lo", 0x26,        Info(0xb0, None, None, None)),
        Item(u"contr_source", 0x16,      Info(0x81, None, None, None)),
        Item(u"p", 0x0a,                 Info(0x82, 0x09, 0x00, 0x03)),
        Item(u"energy_hi", 0x00,         Info(0x82, 0x28, 0x00, 0x7f)),
        Item(u"energy_lo", 0x00,         Info(0xb0, None, None, None)),
        Item(u"speed", 0x50,             Info(0x82, 0x13, 0x00, 0x2e)),
        Item(u"curve_no_ref", 0x0e,      Info(0x80, None, None, None)),
        Item(u"alarm_code", 0x00,        Info(0xa0, None, None, None)),
        Item(u"alarm_log_1", 0x20,       Info(0xa0, None, None, None)),
        Item(u"alarm_log_2", 0x39,       Info(0xa0, None, None, None)),
        Item(u"alarm_log_3", 0x30,       Info(0xa0, None, None, None)),
        Item(u"alarm_log_4", 0x40,       Info(0xa0, None, None, None)),
        Item(u"alarm_log_5", 0x00,       Info(0xa0, None, None, None)),
        Item(u"unit_family", 0x07,       Info(0x80, None, None, None)),
        Item(u"unit_type", 0x01,         Info(0x80, None, None, None)),
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
        Item(u"unit_addr",         0xe7, Info(0xa0, None, None, None)),
        Item(u"group_addr",        0xf7, Info(0xa0, None, None, None)),
        Item(u"min_curve_no",      0x00, Info(0x80, None, None, None)),

        Item(u"h_const_ref_min",   0x17, Info(0x82, 0x19, 0x00, 0x0b)),
        Item(u"h_const_ref_max",   0xd0, Info(0x82, 0x19, 0x00, 0x0b)),
        Item(u"h_prop_ref_min",    0x17, Info(0x82, 0x19, 0x00, 0x0b)),
        Item(u"h_prop_ref_max",    0xd0, Info(0x82, 0x19, 0x00, 0x0b)),

        Item(u"ref_steps",         0x51, Info(0x80, None, None, None)),
    },

    defs.ADPUClass.REFERENCE_VALUES: {
        Item(u"ref_rem",        0x10,    Info(0x80, None, None, None)),
        Item(u"ref_ir",         0x20,    Info(0x82, 0x1e, 0x00, 0x64)),
        Item(u"ref_att_rem",    0x30,    Info(0x80, None, None, None)),
    },
    defs.ADPUClass.ASCII_STRINGS: {},
}


def getParameterValue(name):
    return [p.value for p in DATA_POOL[defs.ADPUClass.CONFIGURATION_PARAMETERS] if p.name == name][0]


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

