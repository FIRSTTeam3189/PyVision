import sys
import time
from networktables import NetworkTable

import logging
logging.basicConfig(level=logging.DEBUG)

ip = "roboRIO-3189-FRC.local"

NetworkTable.setClientMode()
NetworkTable.setIPAddress(ip)
NetworkTable.initialize()

test = NetworkTable.getTable("test")

def valueChanged(key, value, isNew):
    print("Value Changed: key: '%s' ; value: %s; isNew: %s" % (key, value, isNew))

class ConnectionListener:
    def connected(self, table):
        print("Connected", table)

    def disconnected(self, table):
        print("Disconnected", table)

c_listener = ConnectionListener()
test.addConnectionListener(c_listener)

sd = NetworkTable.getTable("SmartDashboard")
auto_value = sd.getAutoUpdateValue('robotTime', 0)

while True:
    print(auto_value.value)
    test.putString("test2", "suck my vagina")
    time.sleep(1)

