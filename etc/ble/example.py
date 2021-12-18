#!/usr/bin/env python3

import sys
from bluepy import btle
import struct
import binascii

MAX=5

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print("A notification was received: %s" % data)
        print("heart rate is: %i" % int(data[1]))

deviceAddress=str(sys.argv[1])
print("Connecting to: %s" % deviceAddress)

# encapsulates a connection to a Bluetooth LE peripheral
peripheral = btle.Peripheral(deviceAddress, btle.ADDR_TYPE_RANDOM)

print("Getting services...")
# Returns a list of Service objects representing the services offered by the peripheral
# A Service object represents a collection of characteristics and descriptors which are
# all related to one particular function of the peripheral.
for service in peripheral.getServices():
    print(str(service))
    print("UUID for this service: %s" % service.uuid)
     # Returns List of Characteristic objects, each represents a short data item which can be read or written
    for characteristic in service.getCharacteristics():
        print("Characteristic: %s" % str(characteristic))
        print("UUID for this characteristic: %s" % characteristic.uuid)
        print("properties as string: %s"  % characteristic.propertiesToString())
        if "NOTIFY" in characteristic.propertiesToString():
            print("establishing subscription")
            try:
                setup_data = b"\x01\x00"
                notify_handle = characteristic.getHandle()
                peripheral.writeCharacteristic(notify_handle+1, setup_data, withResponse=True)
            except BTLEException:
                print("BTLEException raised writing characteristic")

        if characteristic.supportsRead():
            try:
                characteristicValue = characteristic.read()
                print("(little) value as int: %i" % int.from_bytes(characteristicValue, "little"))
                print("   (big) value as int: %i" % int.from_bytes(characteristicValue, "big"))
                print("      value as string: %s" % characteristicValue.decode())
            except UnicodeError:
                print("Characteristic is not UTF-8")
        print("\n")


peripheral.withDelegate(MyDelegate())
for i in range(MAX):
    if peripheral.waitForNotifications(1.0):
        continue
    if i == MAX:
        sys.exit("Exiting...")
    print("Waiting...")

print("Disconnecting from: %s" % deviceAddress)
peripheral.disconnect()