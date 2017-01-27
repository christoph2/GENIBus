#!/usr/bin/env python

import abc
import unittest
import types

class Subject(object):
    def __init__(self, obj):
        self.observers = set()
        self._obj = obj

    def registerObserver(self, observer):
        self.observers.add(observer)

    def removeObserver(self, observer):
        self.observers.discard(observer)

    def notifyObservers(self):
        map(lambda observer: observer.update(self._obj),[o for o in self.observers])



class IObserver(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def update(self, obj):
        pass

##
##  UNIT-TESTS.
##

class MySubject(Subject):
    def __init__(self, name):
        super(MySubject, self).__init__(self)
        self.name = name


class MyObserver(IObserver):
    def __init__(self, name):
        self.name = name

    def update(self, obj):
        pass
        # print("MyObserver(%s): % s was updated." % (self.name, obj.name))


obs1 = MyObserver("1")
obs2 = MyObserver("2")
obs3 = MyObserver("3")

sub1 = MySubject("foo")
sub2 = MySubject("bar")

sub1.registerObserver(obs1)
sub1.registerObserver(obs2)
sub1.registerObserver(obs3)
sub1.notifyObservers()
sub1.removeObserver(obs2)
sub1.notifyObservers()

sub1.registerObserver(obs2)
sub2.registerObserver(obs2)
sub2.notifyObservers()


class TestCases(unittest.TestCase):
    def testFirst(self):
        pass

def main():
    unittest.main()

if __name__ == '__main__':
    main()

