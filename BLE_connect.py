from bluepy.btle import Peripheral, Scanner, DefaultDelegate
import bluepy
import binascii
import struct
import time

##################################################
### GLOBAL VARIABLES
##################################################
IMU_MAC_ADDRESS = "ff:3c:8f:22:c9:c8"

##################################################
### UUIDs
##################################################
UUID_NAME = "00002a00-0000-1000-8000-00805f9b34fb"
UUID_DATA = "2d30c082-f39f-4ce6-923f-3484ea480596"


imu = Peripheral(IMU_MAC_ADDRESS, "random")
characteristics = imu.getCharacteristics()
print("Available characteristics:")
for c in characteristics:
    print(c.uuid)


device_name = (imu.getCharacteristics(uuid=UUID_NAME)[0]).read()
device_name = device_name.decode('UTF-8')
print ("Device name: ", device_name)

"""
print("Acceleration:")
while(True):
    rawdata = (imu.getCharacteristics(uuid=UUID_DATA)[0]).read()
    ax = struct.unpack('f', rawdata)[0]
    rawdata = (imu.getCharacteristics(uuid=UUID_DATA)[0]).read()
    ay = struct.unpack('f', rawdata)[0]
    rawdata = (imu.getCharacteristics(uuid=UUID_DATA)[0]).read()
    az = struct.unpack('f', rawdata)[0]
    print (ax, ay, az)
"""
