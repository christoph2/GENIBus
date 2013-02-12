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
## Asynchronous part of model.
##

import logging
import threading
import time
import sys

if sys.version_info.major > 2:
    import queue
else:
    import Queue as queue

import genicontrol.apdu as apdu
import genicontrol.defs as defs
from genicontrol.dissect import dissectResponse
from genicontrol.utils import dumpHex
import genicontrol.dataitems as dataitems

class PendingRequestError(Exception): pass
class RequestTimeoutError(Exception): pass


MAX_RETRIES             = 10
CYCLE_TIME_STARTUP      = 0.1
CYCLE_TIME_OPERATIONAL  = 0.5

class WorkerThread(threading.Thread):
    logger = logging.getLogger("genicontrol")

    def __init__(self, request, requestorThread):
        super(WorkerThread, self).__init__()
        self._request = request
        self._requestorThread = requestorThread
        self.setName(self.__class__.__name__)

    def run(self):
        name = self.getName()
        resp = self._requestorThread.readFromServer()
        if resp:    # todo: Exception.
            self._requestorThread._respQueue.put(resp)


class RequestorThread(threading.Thread):
    STATE_IDLE          = 0
    STATE_CONNECT       = 1
    STATE_REQ_INFO      = 2
    STATE_REQ_REFS      = 3
    STATE_REQ_PARAM     = 4
    STATE_REQ_STRING    = 5
    STATE_OPERATIONAL   = 6

    _clsLock = threading.Lock()
    _respQueue = queue.Queue()
    _requestQueue = queue.Queue()
    _currentRequest = None
    _currentResponse = None
    logger = logging.getLogger("genicontrol")

    def __new__(cls, *args):
        try:
            cls._clsLock.acquire()
            if not hasattr(cls, '_instance'):
                cls._state = cls.STATE_IDLE
                cls._instance = super(cls.__class__, cls).__new__(cls)
        finally:
            cls._clsLock.release()
        return cls._instance


    def __init__(self, model):
        super(RequestorThread, self).__init__()
        self.setName(self.__class__.__name__)
        self._connected = False
        self._currentRetry = 0
        self._model = model
        self._requestedDatapoints = []
        self._lastCalled = time.clock()
        self._cycleTime = CYCLE_TIME_STARTUP

    def run(self):
        self._model.waitForController()
        name = self.getName()
        self.logger.info("Starting %s." % name)
        while True:
            if self.getState() == RequestorThread.STATE_IDLE:
                self.setState(RequestorThread.STATE_CONNECT)
                self.logger.info('Trying to connect to %s.' % self._model.TYPE)
                self._currentRetry += 1
                self._model.connect()
            elif self.getState() == RequestorThread.STATE_REQ_INFO:
                if self._infoRequests:
                    req, self._requestedDatapoints = self._infoRequests.pop()
                    self._model.requestInfo(req)
                else:
                    self.setState(RequestorThread.STATE_REQ_REFS)
            else:
                pass
            res = self._model._quitEvent.wait(self._cycleTime)
            if res:
                self.logger.info("Exiting %s." % name)
                break

    def request(self, req):
        RequestorThread._currentRequest = req
        self.writeToServer(req)
        self.worker = WorkerThread(req, self)
        self.worker.start()
        success = True
        try:
            data = RequestorThread._respQueue.get(True, 1.0)
        except queue.Empty:
            success = False
        if not success:
            self.logger.info("Timed out.")
        else:
            response = dissectResponse(data)
            if self.getState() == RequestorThread.STATE_CONNECT:
                self.setState(RequestorThread.STATE_REQ_INFO)
                self.processConnectResp(response)
                self._infoRequests = createInfoRequestTelegrams(self._model.getUnitAddress())
            elif self.getState() == RequestorThread.STATE_REQ_INFO:
                #print "Processing INFO Response: ", response, self._requestedDatapoints
                result = interpreteInfoResponse(response, self._requestedDatapoints)
                self._model.updateInfoDict(result)
            else:
                pass

    def processConnectResp(self, response):
        unitAddress = response.sa
        for apdu in response.APDUs:
            if apdu.klass == defs.ADPUClass.PROTOCOL_DATA:
                df_buf_len, unit_bus_mode = apdu.data
                self.setValue(defs.ADPUClass.PROTOCOL_DATA, 'df_buf_len', df_buf_len)
                self.setValue(defs.ADPUClass.PROTOCOL_DATA, 'unit_bus_mode', unit_bus_mode)
            elif apdu.klass == defs.ADPUClass.CONFIGURATION_PARAMETERS:
                unit_addr, group_addr = apdu.data
                self.setValue(defs.ADPUClass.CONFIGURATION_PARAMETERS, 'unit_addr', unit_addr)
                self.setValue(defs.ADPUClass.CONFIGURATION_PARAMETERS, 'group_addr', group_addr)
            elif apdu.klass == defs.ADPUClass.MEASURERED_DATA:
                unit_family, unit_type = apdu.data
                self.setValue(defs.ADPUClass.MEASURERED_DATA, 'unit_family', unit_family)
                self.setValue(defs.ADPUClass.MEASURERED_DATA, 'unit_type', unit_type)
        self.logger.info('OK, Connected.')

    def writeToServer(self, req):
        self._model.writeToServer(req)

    def readFromServer(self):
        return self._model.readFromServer()

    def setValue(self, group, datapoint, value):
        self._model.setValue(group, datapoint, value)

    def _getRequestQueue(self):
        return self._requestQueue

    def setState(self, state):
        self._state = state

    def getState (self):
        return self._state

    def clockDiff(self):
        return time.clock() - self._lastCalled

    requestQueue = property(_getRequestQueue)



MAX_INFO_REQUESTS = 15
##
## GeniBus guarantees a minimun telegeram length of 70 bytes.
## 8 bytes are fixed per info-response, 1 - 4 bytes per datapoint:
##      8 + (4 * n) = 70
##      n = 15


def createInfoRequestTelegrams(destAddr):
    ##
    ## Info responses contain vital information like physical units and scaling stuff.
    ##
    result = []
    dd = dict.fromkeys(set([x.klass for x in dataitems.DATAITEMS if not (x.klass in (0, 3, 7))]))
    for key in dd.keys():
        dd[key] = dict()
    for item in dataitems.DATAITEMS:
        name, klass, _id, _, _ = item
        if klass not in (defs.ADPUClass.MEASURERED_DATA, defs.ADPUClass.REFERENCE_VALUES, defs.ADPUClass.CONFIGURATION_PARAMETERS):
            continue
        dd[klass][name] = _id
    for klass, items in dd.items():
        items = items.items()
        if len(items) > MAX_INFO_REQUESTS:
            slices = [items [i : i + MAX_INFO_REQUESTS] for i in range(0, len(items), MAX_INFO_REQUESTS)]
        else:
            slices = [items]
        for idx, slice in enumerate(slices):
            slice = [n for n,i in slice]
            if klass == defs.ADPUClass.MEASURERED_DATA:
                telegram = apdu.createGetInfoPDU(apdu.Header(defs.SD_DATA_REQUEST, destAddr, 0x04), measurements = slice)
            elif klass == defs.ADPUClass.REFERENCE_VALUES:
                telegram = apdu.createGetInfoPDU(apdu.Header(defs.SD_DATA_REQUEST, destAddr, 0x04), references = slice)
            elif klass == defs.ADPUClass.CONFIGURATION_PARAMETERS:
                telegram = apdu.createGetInfoPDU(apdu.Header(defs.SD_DATA_REQUEST, destAddr, 0x04), parameter = slice)
            result.append((telegram, slice, ))
    return result


def interpreteInfoResponse(response, datapoints):
    result = dict()
    for apdu in response.APDUs:
        klass = apdu.klass
        result.setdefault(klass, {})
        idx = 0
        values = []
        for datapoint in datapoints:
            data = apdu.data[idx]
            sif = data & 0b11
            if sif in (0, 1):
                result[klass][datapoint] = defs.Info(data, None, None, None)
                idx += 1    # No scaling information.
            else:
                result[klass][datapoint] = defs.Info(data, apdu.data[idx + 1], apdu.data[idx + 2], apdu.data[idx + 3])
                idx += 4
    return result


def main():
    fin  = threading.Event()
    req = RequestorThread(fin)
    req.start()
    time.sleep(10)
    fin.set()
    req.join()

if __name__ == '__main__':
    main()

"""
def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()

q = Queue()
for i in range(num_worker_threads):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

for item in source():
    q.put(item)

q.join()
"""

