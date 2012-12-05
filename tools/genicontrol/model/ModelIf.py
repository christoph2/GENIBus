#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
#import genicontrol.observer as observer
from wx.lib.pubsub import Publisher as Publisher

DATA_NOT_AVAILABLE = 0xff

class IModel(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        #super(IModel, self).__init__(self)
        self._pub = Publisher()
        self.initialize()

    def sendMessage(self, topic, data):
        self._pub.sendMessage(topic,data)

    def subscribe(self, topic, callback):
        self._pub.subscribe(topic = topic, listener = callback)

    @abc.abstractmethod
    def initialize(self):
        pass

    ## todo: getListOf MeasurementValues, etc.

    @abc.abstractmethod
    def connect(self, *parameters):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass

    @abc.abstractmethod
    def requestMeasurementValues(self):
        pass

    @abc.abstractmethod
    def requestParameters(self):
        pass

    @abc.abstractmethod
    def requestReferences(self):
        pass

    @abc.abstractmethod
    def requestInfo(self):
        pass

    @abc.abstractmethod
    def setReferenceValue(self, item, value):
        pass

    @abc.abstractmethod
    def setParameterValue(self, item, value):
        pass

    @abc.abstractmethod
    def sendCommand(self, command):
        pass


