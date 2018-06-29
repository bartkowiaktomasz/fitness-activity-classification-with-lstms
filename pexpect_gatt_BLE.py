# Run with
# sudo /home/tomasz/anaconda3/bin/python pexpect_gatt_BLE.py
# since sudo uses different python version (see "$ sudo which python")

import pexpect
import struct
import time
import sys

import visualize as vis

##################################################
### GLOBAL VARIABLES
##################################################
IMU_MAC_ADDRESS = "FF:3C:8F:22:C9:C8"
UUID_DATA = "2d30c082-f39f-4ce6-923f-3484ea480596"

##### READINGS LIST
ax_readings = []
ay_readings = []
az_readings = []

##################################################
### MAIN
##################################################
if __name__ == '__main__':
    gatt = pexpect.spawn("gatttool -t random -b " + IMU_MAC_ADDRESS + " -I")
    gatt.sendline("connect")
    gatt.expect("Connection successful")

    # Counter for the graph
    count = 0
    while(True):
        gatt.sendline("char-read-uuid " + UUID_DATA)
        gatt.expect("handle: 0x0011 	 value: ")
        gatt.expect(" \r\n")
        rawdata = (gatt.before).decode('UTF-8').strip(' ').split(' ')

        ax_raw = (rawdata[0] + rawdata[1] + rawdata[2] + rawdata[3])
        ay_raw = (rawdata[4] + rawdata[5] + rawdata[6] + rawdata[7])
        az_raw = (rawdata[8] + rawdata[9] + rawdata[10] + rawdata[11])

        ax = struct.unpack('f', bytes.fromhex(ax_raw))[0]
        ay = struct.unpack('f', bytes.fromhex(ay_raw))[0]
        az = struct.unpack('f', bytes.fromhex(az_raw))[0]

        print(ax, ay, az)

        ax_readings.append(ax)
        ay_readings.append(ay)
        az_readings.append(az)

        vis.drawGraphs(ax_readings, ay_readings, ay_readings)

        count += 1
        if(count > 50):
            ax_readings.pop(0)
            ay_readings.pop(0)
            az_readings.pop(0)
