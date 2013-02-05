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

import logging
import threading
import time
import sys

if sys.version_info.major > 2:
    import queue
else:
    import Queue as queue

import genicontrol.apdu as apdu
from genicontrol.utils import dumpHex

class PendingRequestError(Exception): pass
class RequestTimeoutError(Exception): pass


MAX_RETRIES = 10

class WorkerThread(threading.Thread):
    logger = logging.getLogger("genicontrol")

    def __init__(self, req, resp, respQueue, cancelEvent):
        super(WorkerThread, self).__init__()
        self._request = req
        self._response = resp
        self._respQueue = respQueue
        self._cancelEvent = cancelEvent
        self.setName(self.__class__.__name__)

    def run(self):
        name = self.getName()
        #self.logger.info("Starting %s." % name)
        while True:
            if self._cancelEvent.wait(1.0):
                break
        #self._respQueue.put([])
        #self._cancelEvent.wait(2.0)
        #self.logger.info("Exiting %s." % name)


class RequestorThread(threading.Thread):
    IDLE    = 0
    PENDING = 1
    TIMEOUT = 2
    _clsLock = threading.Lock()
    _respQueue = queue.Queue()
    _requestQueue = queue.Queue()
    _cancelEvent = threading.Event()
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
                self.cancelWorkerThread()
                break
            if RequestorThread._state == RequestorThread.IDLE:
                pass
                #self.request([])

    def cancelWorkerThread(self):
        if hasattr(self, 'worker'):
            RequestorThread._cancelEvent.set()
            self.worker.join()

    def request(self, req):
        RequestorThread._state = RequestorThread.PENDING
        RequestorThread._currentRequest = req
        self.worker = WorkerThread(req, RequestorThread._currentResponse, RequestorThread._respQueue, RequestorThread._cancelEvent)
        self.worker.start()
        print "Doing request. '%s'" % dumpHex(req)
        success = True
        try:
            response = RequestorThread._respQueue.get(True, 0.5)
        except queue.Empty:
            success = False
        if not success:
            #self.logger.info("Cancelling %s." % self.worker.getName())
            self.cancelWorkerThread()
            #RequestorThread._cancelEvent.clear()
        else:
            print "Processing Response."
        RequestorThread._state = RequestorThread.IDLE

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

