from bluepy.btle import Peripheral
import numba
from numba import jit
from numpy import arange

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

##################################################
### FUNCTIONS
##################################################
@jit
def readIMUdata(uuid):
    while(True):
        start = time.time()
        rawdata1 = (imu.getCharacteristics(uuid=UUID_DATA)[0]).read()
        print(time.time() - start)
        rawdata2 = (imu.getCharacteristics(uuid=UUID_DATA)[0]).read()
        rawdata3 = (imu.getCharacteristics(uuid=UUID_DATA)[0]).read()
        ax = struct.unpack('f', rawdata1)[0]
        ay = struct.unpack('f', rawdata2)[0]
        az = struct.unpack('f', rawdata3)[0]
        print (ax, ay, az)


if __name__ == '__main__':

    imu = Peripheral(IMU_MAC_ADDRESS, "random")
    characteristics = imu.getCharacteristics()
    print("Available characteristics:")
    for c in characteristics:
        print(c.uuid)

    device_name = (imu.getCharacteristics(uuid=UUID_NAME)[0]).read()
    device_name = device_name.decode('UTF-8')
    print ("Device name: ", device_name)

    print("Acceleration:")
    readIMUdata(UUID_DATA)
