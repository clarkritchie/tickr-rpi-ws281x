#!/usr/bin/env python3

import random
from singleton import Singleton

@Singleton
class TickrMock:
    beats = 100
    deviceAddress = ""

    def connect(self, address):
        print("Connecting to: %s" % address)
        self.deviceAddress = address

    def subscribe(self):
        print("Subscribe to BTLE device")

    def disconnect(self):
        print("Disconnecting from: %s" % self.deviceAddress)

    def get_heart_rate(self):
        # just return some data to allow the Strand to be called
        # range is to prevent jumping around too much in any one call
        delta = 10
        min = 50
        max = 180
        b = random.randint(self.beats-delta, self.beats+delta)
        if b <= min:
            b = min
        if b > max:
            b = max
        self.beats = b
        return self.beats

    def __init__(self):
        print("TickrMock constructor")
