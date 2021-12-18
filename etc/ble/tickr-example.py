#!/usr/bin/env python3

# this is a very simple example to pull heart rate data from a Wahoo TICKR
# given a MAC address
# connects to the device
# print out what it can do
# subscribe to the heart rate
# receive data and print it out

import sys
from bluepy import btle

# maximum number of subscription polls
MAX=10

class TICKRDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print("A notification was received: %s" % data)
        # TICKR heart rate data is the second item
        if len(data) >= 1:
            print("Heart rate is: %i" % int(data[1]))

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
        print("Characteristic's UUID: %s" % characteristic.uuid)
        print("Characteristic's properties: %s"  % characteristic.propertiesToString())
        if "NOTIFY" in characteristic.propertiesToString():
            print("Establishing subscription ")
            try:
                # toggle the bit that allows us to establish a subscription
                setup_data = b"\x01\x00"
                notify_handle = characteristic.getHandle()
                peripheral.writeCharacteristic(notify_handle+1, setup_data, withResponse=True)
            except btle.BTLEException:
                print("BTLEException raised writing characteristic")

        if characteristic.supportsRead():
            try:
                characteristicValue = characteristic.read()
                print("Characteristic value: %s" % characteristicValue.decode())
            except UnicodeError:
                print("Characteristic is not UTF-8")
        print("\n")

peripheral.withDelegate(TICKRDelegate())
for i in range(MAX):
    if peripheral.waitForNotifications(1.0):
        continue
    if i >= MAX:
        sys.exit("Exiting...")
    else:
        print("Waiting...")

print("Disconnecting from: %s" % deviceAddress)
peripheral.disconnect()