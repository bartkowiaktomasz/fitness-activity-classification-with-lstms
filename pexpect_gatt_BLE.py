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

# Data type sent from the device
DATA_TYPE = 'h'
DATA_SIZE_BYTES = 2

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

        shift = 0
        ax_raw = (rawdata[shift + 0] + rawdata[shift + 1])
        shift = 1 * DATA_SIZE_BYTES
        ay_raw = (rawdata[shift + 0] + rawdata[shift + 1])
        shift = 2 * DATA_SIZE_BYTES
        az_raw = (rawdata[shift + 0] + rawdata[shift + 1])
        shift = 3 * DATA_SIZE_BYTES
        gx_raw = (rawdata[shift + 0] + rawdata[shift + 1])
        shift = 4 * DATA_SIZE_BYTES
        gy_raw = (rawdata[shift + 0] + rawdata[shift + 1])
        shift = 5 * DATA_SIZE_BYTES
        gz_raw = (rawdata[shift + 0] + rawdata[shift + 1])
        shift = 6 * DATA_SIZE_BYTES
        mx_raw = (rawdata[shift + 0] + rawdata[shift + 1])
        shift = 7 * DATA_SIZE_BYTES
        my_raw = (rawdata[shift + 0] + rawdata[shift + 1])
        shift = 8 * DATA_SIZE_BYTES
        mz_raw = (rawdata[shift + 0] + rawdata[shift + 1])

        ax = struct.unpack(DATA_TYPE, bytes.fromhex(ax_raw))[0]
        ay = struct.unpack(DATA_TYPE, bytes.fromhex(ay_raw))[0]
        az = struct.unpack(DATA_TYPE, bytes.fromhex(az_raw))[0]

        # Scale to the same range as WISDM dataset
        ax = ax/100
        ay = ay/100
        az = az/100

        print(ax, ay, az)

        ax_readings.append(ax)
        ay_readings.append(ay)
        az_readings.append(az)

        vis.drawGraphs(ax_readings, ay_readings, az_readings)

        count += 1
        if(count > 50):
            ax_readings.pop(0)
            ay_readings.pop(0)
            az_readings.pop(0)
