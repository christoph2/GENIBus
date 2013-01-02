#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2012 by Christoph Schueler <github.com/Christoph2,
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

#import genicontrol.model.ModelIf
import ModelIf
from genicontrol.model.config import DataitemConfiguration
import genicontrol.dataitems as dataitems

#from wx.lib.pubsub import Publisher as Publisher

class NullModel(ModelIf.IModel):

    def initialize(self):
        for idx, item in enumerate(DataitemConfiguration['MeasurementValues']):
            key, displayName, unit, controlID = item
            ditem =  dataitems.MEASUREMENT_VALUES[key]
            self.sendMessage('Measurements.%s' % key, ModelIf.DATA_NOT_AVAILABLE)
        self.sendMessage('References', ModelIf.DATA_NOT_AVAILABLE)
        self.dataAvailable = False

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


##
##nm = NullModel()
###nm.beatEvent()
##class Observer(object):
##    def __init__(self, model):
##        self._model = model
##        model.subscribe('Measurements', self.onChange)
##        model.subscribe('References', self.onChange)
##
##    def onChange(self, msg):
##        print msg.topic, msg.data
##        print str(msg)
##
##
##obs = Observer(nm)
##nm.sendMessage('Measurements', ModelIf.DATA_NOT_AVAILABLE)
##nm.sendMessage('References', ModelIf.DATA_NOT_AVAILABLE)
##

