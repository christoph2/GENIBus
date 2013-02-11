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

class PendingRequestError(Exception): pass
class RequestTimeoutError(Exception): pass


MAX_RETRIES = 10

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
    IDLE    = 0
    PENDING = 1
    TIMEOUT = 2
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
                cls._state = cls.IDLE
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

        self._lastCalled = time.clock()

    def run(self):
        self._model.waitForController()
        name = self.getName()
        self.logger.info("Starting %s." % name)
        while True:
            if not self._connected:
                self.logger.info('Trying to connect to %s.' % self._model.TYPE)
                self._currentRetry += 1
                self._model.connect()
            res = self._model._quitEvent.wait(.5)
            if res:
                self.logger.info("Exiting %s." % name)
                break
            if RequestorThread._state == RequestorThread.IDLE:
                pass
                #self.request([])

    def request(self, req):
        RequestorThread._state = RequestorThread.PENDING
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
            if not self._connected:
                self.processConnectResp(response)
            else:
                pass
        RequestorThread._state = RequestorThread.IDLE

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
        self._connected = True
        self.logger.info('OK, Connected.')

    def writeToServer(self, req):
        self._model.writeToServer(req)

    def readFromServer(self):
        return self._model.readFromServer()

    def setValue(self, group, datapoint, value):
        self._model.setValue(group, datapoint, value)

    def _getRequestQueue(self):
        return self._requestQueue

    def clockDiff(self):
        return time.clock() - self._lastCalled

    requestQueue = property(_getRequestQueue)

def buildLPDU():
    pass


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

