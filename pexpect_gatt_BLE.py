import pexpect
import struct
import time
import sys

##################################################
### GLOBAL VARIABLES
##################################################
IMU_MAC_ADDRESS = "FF:3C:8F:22:C9:C8"
UUID_DATA = "2d30c082-f39f-4ce6-923f-3484ea480596"

SLEEP = 0.1

##################################################
### MAIN
##################################################
if __name__ == '__main__':
    gatt = pexpect.spawn("gatttool -t random -b " + IMU_MAC_ADDRESS + " -I")
    gatt.sendline("connect")
    gatt.expect("Connection successful")

    while(True):
        gatt.sendline("char-read-uuid " + UUID_DATA)
        gatt.expect("handle: 0x0011 	 value: ")
        gatt.expect(" \r\n")
        data = gatt.before
        print(data)
        # ax = (gatt.before).decode('UTF-8').replace(" ", "").decode('hex')

        # print(struct.unpack('f', ax)[0])
