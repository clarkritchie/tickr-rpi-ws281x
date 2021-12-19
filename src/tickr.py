#!/usr/bin/env python3

import sys, random, threading, logging, os
logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO').upper())
from singleton import Singleton
from bluepy import btle

class TickrDelegate(btle.DefaultDelegate):
    data = None
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        logging.debug("A notification was received: %s" % data)
        # heart rate data is the second item
        if len(data) >= 1:
            beats = int(data[1])
            logging.debug("Heart rate is: %i" % beats)
            self.data = beats

    def get_data(self):
        return self.data

@Singleton
class Tickr:

    th = None
    beats = 0
    deviceAddress = ""
    peripheral = None
    fetch_data = False
    HRM_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

    def connect(self, address):
        logging.debug("Connecting to: %s" % address)
        self.deviceAddress = address
        self.peripheral = btle.Peripheral(self.deviceAddress, btle.ADDR_TYPE_RANDOM)

    def _subscribe(self):
        logging.debug("Subscribing to BTLE device")

        for service in self.peripheral.getServices():
#             logging.debug(str(service))
#             logging.debug("UUID for this service: %s" % service.uuid)
             # Returns List of Characteristic objects, each represents a short data item which can be read or written
            for characteristic in service.getCharacteristics():
                if "NOTIFY" in characteristic.propertiesToString():
#                     logging.debug("Characteristic: %s" % str(characteristic))
#                     logging.debug("  UUID: %s" % characteristic.uuid)
#                     logging.debug("  Properties: %s" % characteristic.propertiesToString())

                    # TODO revisit this
                    if (characteristic.uuid == self.HRM_UUID):
                        logging.debug("Establishing subscription to HRM")
                        try:
                            # toggle the bit that allows us to establish a subscription
                            setup_data = b"\x01\x00"
                            notify_handle = characteristic.getHandle()
                            self.peripheral.writeCharacteristic(notify_handle+1, setup_data, withResponse=True)

                            delegate = TickrDelegate()
                            self.peripheral.withDelegate(delegate)

                            while self.fetch_data:
                                if self.peripheral.waitForNotifications(1.0):
                                    self.beats = delegate.get_data()
                                    logging.info("Beats are %s" % self.beats)
                                    continue
                                else:
                                    logging.debug("Waiting...")

                        except btle.BTLEException:
                            logging.debug("BTLEException raised writing characteristic")

    def subscribe(self):
        self.fetch_data = True
        self.th = threading.Thread(target=self._subscribe, daemon=True)
        self.th.start()

    def disconnect(self):
        logging.debug(f"Disconnecting...")
        logging.debug(f"is thread alive? {self.th.is_alive()}")
        self.fetch_data = False
        self.th.join()
        logging.debug(f"is thread still alive? {self.th.is_alive()}")
        logging.info("Disconnecting from: %s" % self.deviceAddress)
        self.peripheral.disconnect()

    def get_heart_rate(self):
        return self.beats

    def __init__(self):
        logging.info("Tickr constructor")