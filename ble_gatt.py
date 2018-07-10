# Run with
# sudo /home/tomasz/anaconda3/bin/python ble_gatt.py
# since sudo uses different python version (see "$ sudo which python")

import pexpect
import struct
import time
import sys
import glob

import pandas as pd

import visualize as vis
from config import * # Global variables

##################################################
### GLOBAL VARIABLES
##################################################

##### READINGS LIST
ax_readings = []
ay_readings = []
az_readings = []
mx_readings = []
my_readings = []
mz_readings = []
gx_readings = []
gy_readings = []
gz_readings = []

##### READINGS LIST FOR GRAPHS
ax_readings_graph = []
ay_readings_graph = []
az_readings_graph = []

##################################################
### FUNCTIONS
##################################################
def extract(rawdata):
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
    gx = struct.unpack(DATA_TYPE, bytes.fromhex(gx_raw))[0]
    gy = struct.unpack(DATA_TYPE, bytes.fromhex(gy_raw))[0]
    gz = struct.unpack(DATA_TYPE, bytes.fromhex(gz_raw))[0]
    mx = struct.unpack(DATA_TYPE, bytes.fromhex(mx_raw))[0]
    my = struct.unpack(DATA_TYPE, bytes.fromhex(my_raw))[0]
    mz = struct.unpack(DATA_TYPE, bytes.fromhex(mz_raw))[0]

    return ax, ay, az, gx, gy, gz, mx, my, mz

def gatt_handshake():
    gatt = pexpect.spawn("gatttool -t random -b " + IMU_MAC_ADDRESS + " -I")
    gatt.sendline("connect")
    gatt.expect("Connection successful")

    return gatt

def gatt_read(gatt):
    gatt.sendline("char-read-uuid " + UUID_DATA)
    gatt.expect("handle: 0x0011 	 value: ")
    gatt.expect(" \r\n")

    rawdata = (gatt.before).decode('UTF-8').strip(' ').split(' ')
    return rawdata

def runWebBLE(activity):
    ax_readings = []
    ay_readings = []
    az_readings = []
    mx_readings = []
    my_readings = []
    mz_readings = []
    gx_readings = []
    gy_readings = []
    gz_readings = []

    gatt = gatt_handshake()

    graph_counter = 0
    activity_list = []
    if(activity not in LABELS_NAMES):
        print("Error: Wrong activity")
        exit()
    print("Selected activity: ", activity)

    inner_loop_counter = 0
    while(inner_loop_counter < DATA_COLLECTION_TIME):
        rawdata = gatt_read(gatt)
        ax, ay, az, gx, gy, gz, mx, my, mz = extract(rawdata)

        # Scale to the same range as WISDM dataset
        ax = ax/SCALE_FACTOR
        ay = ay/SCALE_FACTOR
        az = az/SCALE_FACTOR

        print("Acceleration x, y, z: ", ax, ay, az)
        # print("Gyroscope x, y, z: ", gx, gy, gz)
        # print("Magnetometer x, y, z: ", mx, my, mz)

        ax_readings.append(ax)
        ay_readings.append(ay)
        az_readings.append(az)
        gx_readings.append(gx)
        gy_readings.append(gy)
        gz_readings.append(gz)
        mx_readings.append(mx)
        my_readings.append(my)
        mz_readings.append(mz)

        inner_loop_counter += 1

    activity_list += [activity for _ in range(DATA_COLLECTION_TIME)]
    data_dict = {
                'activity': activity_list, 'acc-x-axis': ax_readings,
                'acc-y-axis': ay_readings, 'acc-z-axis': az_readings, \
                'gyro-x-axis': gx_readings, 'gyro-y-axis': gy_readings, \
                'gyro-z-axis': gz_readings, 'mag-x-axis': mx_readings, \
                'mag-y-axis': my_readings, 'mag-z-axis': mz_readings
                 }
    data_frame = pd.DataFrame(data=data_dict)

    num_files = len(glob.glob(DATA_TEMP_DIR + '*.pckl'))
    data_frame.to_pickle('data_temp/sample_{}_{}.pckl'.format(activity, num_files + 1))

def runBLE():
    from model_test_tf import preprocess_evaluate

    gatt = gatt_handshake()
    print("How many samples do you want to collect?")
    number_samples = input()
    try:
        number_samples = int(number_samples)
    except ValueError:
        print("Not an integer")
        exit()

    graph_counter = 0
    outer_loop_counter = 0
    activity_list = []
    while(outer_loop_counter < number_samples):
        print("\n\nWhat activity are you going to perform? Type one of the following:")
        for label in LABELS_NAMES:
            print(label)

        activity = input()
        print("Your activity: ", activity)
        if activity not in LABELS_NAMES:
            print("Wrong input, choose again")
            continue

        inner_loop_counter = 0
        while(inner_loop_counter < SEGMENT_TIME_SIZE):
            rawdata = gatt_read(gatt)

            ax, ay, az, gx, gy, gz, mx, my, mz = extract(rawdata)

            # Scale to the same range as WISDM dataset
            ax = ax/SCALE_FACTOR
            ay = ay/SCALE_FACTOR
            az = az/SCALE_FACTOR

            print("Acceleration x, y, z: ", ax, ay, az)
            # print("Gyroscope x, y, z: ", gx, gy, gz)
            # print("Magnetometer x, y, z: ", mx, my, mz)

            ax_readings.append(ax)
            ay_readings.append(ay)
            az_readings.append(az)
            gx_readings.append(gx)
            gy_readings.append(gy)
            gz_readings.append(gz)
            mx_readings.append(mx)
            my_readings.append(my)
            mz_readings.append(mz)

            ax_readings_graph.append(ax)
            ay_readings_graph.append(ay)
            az_readings_graph.append(az)

            # vis.drawGraphs(ax_readings_graph, ay_readings_graph, az_readings_graph)

            graph_counter += 1
            if(graph_counter > 50):
                ax_readings_graph.pop(0)
                ay_readings_graph.pop(0)
                az_readings_graph.pop(0)

            inner_loop_counter += 1

        outer_loop_counter += 1
        activity_list += [activity for _ in range(SEGMENT_TIME_SIZE)]

    data_dict = {
                'activity': activity_list, 'acc-x-axis': ax_readings,
                'acc-y-axis': ay_readings, 'acc-z-axis': az_readings, \
                'gyro-x-axis': gx_readings, 'gyro-y-axis': gy_readings, \
                'gyro-z-axis': gz_readings, 'mag-x-axis': mx_readings, \
                'mag-y-axis': my_readings, 'mag-z-axis': mz_readings
                 }
    data_frame = pd.DataFrame(data=data_dict)

    is_save = input("Do you want to save the sample? [y/n]")
    if(is_save == "y"):
        data_frame.to_pickle('data_temp/sample.pckl')

    is_evaluate = input("Do you want to evaluate (test) the sample? [y/n]")
    if(is_evaluate == "y"):
        preprocess_evaluate(data_frame)

##################################################
### MAIN
##################################################
if __name__ == '__main__':
    runBLE()
