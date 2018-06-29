from bluepy.btle import Peripheral
import numba

# Numba for faster computation
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
UUID_NAME = "00002a00-0000-1000-8000-00805f9b34fb"
UUID_DATA = "2d30c082-f39f-4ce6-923f-3484ea480596"


##################################################
### FUNCTIONS
##################################################
@jit
def readIMUdata(device):
    while(True):
        start = time.time()
        print("getCharacteristics execution time:", time.time() - start)
        rawdata1 = (device.getCharacteristics(uuid=UUID_DATA)[0]).read()
        # rawdata2 = (device.getCharacteristics(uuid=UUID_DATA)[0]).read()
        # rawdata3 = (device.getCharacteristics(uuid=UUID_DATA)[0]).read()
        ax = struct.unpack('i', rawdata1)[0]
        # ay = struct.unpack('f', rawdata2)[0]
        # az = struct.unpack('f', rawdata3)[0]
        print (ax)

##################################################
### MAIN
##################################################
def main():
    imu = Peripheral(IMU_MAC_ADDRESS, "random")
    characteristics = imu.getCharacteristics()
    print("Available characteristics:")
    for c in characteristics:
        print(c.uuid)

    device_name = (imu.getCharacteristics(uuid=UUID_NAME)[0]).read()
    device_name = device_name.decode('UTF-8')
    print ("Device name: ", device_name)

    print("Acceleration:")
    readIMUdata(imu)

main()
