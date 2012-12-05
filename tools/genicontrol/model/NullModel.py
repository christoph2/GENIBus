#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import genicontrol.model.ModelIf
import ModelIf

from wx.lib.pubsub import Publisher as Publisher

class NullModel(ModelIf.IModel):

    def initialize(self):
        self.sendMessage('Measurements', ModelIf.DATA_NOT_AVAILABLE)
        self.sendMessage('References', ModelIf.DATA_NOT_AVAILABLE)

    def connect(self, *parameters):
        pass

    def disconnect(self):
        pass

    def requestMeasurementValues(self):
        pass

    def requestParameters(self):
        pass

    def requestReferences(self):
        pass

    def requestInfo(self):
        pass

    def setReferenceValue(self, item, value):
        pass

    def setParameterValue(self, item, value):
        pass

    def sendCommand(self, command):
        pass

#    def beatEvent(self):
#        self.notifyObservers()


nm = NullModel()
#nm.beatEvent()
class Observer(object):
    def __init__(self, model):
        self._model = model
        #model.subscribe('Measurements', self.onChange())

    def onChange(self, *args, **kwargs):
        print args
        print kwargs


obs = Observer(nm)

