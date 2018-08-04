"""
Library for Bluetooth Low Energy data transfer between the BLE
device and the client. The service used for communication is gatt.
Communication is established via pexpect python library.
"""

# Run with
# sudo /home/tomasz/anaconda3/bin/python ble_gatt.py
# since sudo uses different python version (see "$ sudo which python")

import pexpect
import requests
import struct
import time
import sys
import glob

import pandas as pd

import visualize as vis
from config import * # Global variables

def extract(rawdata):
    """
    Take as input an array of hexadecimal values and unpack it
    into specificed data type (numeric).
    Return a tuple of those numbers (IMU readings).
    """
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
    """
    This function establishes connection with a BLE device using gatt
    service. MAC address of the destination device must be given
    (it is specified in the config file).
    Return a pexpect.spawn object (gatt).
    """
    gatt = pexpect.spawn("gatttool -t random -b " + IMU_MAC_ADDRESS + " -I")
    gatt.sendline("connect")
    gatt.expect("Connection successful")

    return gatt

def gatt_read(gatt):
    """
    Take as input a pexpect object (gatt) returned by pexpect.spawn method.
    Read data from the device using specific uuid (universally unique
    identifier), decode it using UTF-8 decoding scheme and return
    a raw data package (Array of hexadecimal values)
    """
    gatt.sendline("char-read-uuid " + UUID_DATA)
    gatt.expect("handle: " + BLE_HANDLE + " 	 value: ")
    gatt.expect(" \r\n")

    rawdata = (gatt.before).decode('UTF-8').strip(' ').split(' ')
    return rawdata

def collect_data(activity,
                 data_collection_time=DATA_COLLECTION_TIME,
                 visualize=False):
    """
    Take as input:
    - an activity for which data will be collected,
    - data collection time (how many samples will be collected),
    default value: DATA_COLLECTION_TIME (set in the config).
    - boolean (visualize), indicating whether the data should be visualized
    (interactive visualization is discouraged as it introduces serious lag).
    The function returns a (pandas) dataframe (dictionary) with
    collected data.
    """
    ax_readings = []
    ay_readings = []
    az_readings = []
    mx_readings = []
    my_readings = []
    mz_readings = []
    gx_readings = []
    gy_readings = []
    gz_readings = []

    ax_readings_graph = []
    ay_readings_graph = []
    az_readings_graph = []

    gatt = gatt_handshake()
    graph_counter = 0
    activity_list = []
    inner_loop_counter = 0
    while(inner_loop_counter < data_collection_time):
        rawdata = gatt_read(gatt)
        ax, ay, az, gx, gy, gz, mx, my, mz = extract(rawdata)

        # Scale to the same range as WISDM dataset
        ax = ax/SCALE_FACTOR
        ay = ay/SCALE_FACTOR
        az = az/SCALE_FACTOR

        gx = gx/SCALE_FACTOR
        gy = gy/SCALE_FACTOR
        gz = gz/SCALE_FACTOR

        mx = mx/SCALE_FACTOR
        my = my/SCALE_FACTOR
        mz = mz/SCALE_FACTOR

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

        if(visualize):
            ax_readings_graph.append(ax)
            ay_readings_graph.append(ay)
            az_readings_graph.append(az)
            graph_counter += 1
            vis.drawGraphs(ax_readings_graph,
                           ay_readings_graph,
                           az_readings_graph)
            if(graph_counter > 50):
                ax_readings_graph.pop(0)
                ay_readings_graph.pop(0)
                az_readings_graph.pop(0)

        inner_loop_counter += 1

        # Wait some time before next request (BLE sends data too slowly)
        time.sleep(BLE_DATA_COLLECTION_LATENCY)

    activity_list += [activity for _ in range(data_collection_time)]
    data_dict = {
                COLUMN_NAMES[0]: activity_list, COLUMN_NAMES[1]: ax_readings,
                COLUMN_NAMES[2]: ay_readings, COLUMN_NAMES[3]: az_readings, \
                COLUMN_NAMES[4]: gx_readings, COLUMN_NAMES[5]: gy_readings, \
                COLUMN_NAMES[6]: gz_readings, COLUMN_NAMES[7]: mx_readings, \
                COLUMN_NAMES[8]: my_readings, COLUMN_NAMES[9]: mz_readings
                }
    data_frame = pd.DataFrame(data=data_dict)
    return data_frame


def web_collect_save_data(activity):
    """
    Interface function for the web client (data collection).
    Client (flask app) revokes this function with a particular
    activity as an input (i.e. "Pushup"). The function establishes
    contact with a BLE device, collects the data and saves in a .pckl
    format.
    The function does not return anything.
    """
    if(activity not in LABELS_NAMES):
        print("Error: Wrong activity")
        exit()
    print("Selected activity: ", activity)

    data_frame = collect_data(activity)

    # Save sample
    num_files = len(glob.glob(DATA_TEMP_DIR + '*.pckl'))
    data_frame.to_pickle('data_temp/sample_{}_{}.pckl'.format(activity, num_files + 1))
    print("----- ACTIVITY SAVED ----\n" * 20)

def web_collect_request():
    """
    Interface function for the web client (activity predictor).
    Client (web app) revokes this function to begin the collection
    of data. Once collected, data is packed into a JSON payload and
    sent via HTTP POST request to the external server that performs
    the classification.
    The function returns a reponse from the server.
    """
    # Set activity just to allow functions to use the data for classification
    dummy_activity = LABELS_NAMES[0]
    df = collect_data(dummy_activity, data_collection_time=SEGMENT_TIME_SIZE)
    df_json = df.to_json()
    payload = {PAYLOAD_KEY: df_json}

    # Make a HTTP request with a json payload
    r = requests.post(IP_ADDRESS, payload)
    return r.text
