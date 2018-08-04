"""
Library for data preprocessing.
"""

import numpy as np
import pandas as pd

from scipy import stats

from config import * # Global variables

def get_convoluted_data(data,
                        segment_time_size=SEGMENT_TIME_SIZE,
                        time_step=TIME_STEP):
    """
    Take as input pandas dataframe and return a tuple: convoluted data and labels.
    Convoluted data is basically the data extracted by sliding a window of size
    SEGMENT_TIME_SIZE with stepsize TIME_STEP. Each window is assigned with one
    label, which is the most frequently occuring label for in given window.
    """
    data_convoluted = []
    labels = []

    increment = 0
    if(len(data) == segment_time_size):
        increment = 1
    elif(len(data) < segment_time_size):
        raise ValueError

    # Slide a "segment_time_size" wide window with a step size of "TIME_STEP"
    #   Increment allows the loop to run if there is just one sample, for which
    #   len(data) == segment_time_size
    for i in range(0, len(data) - segment_time_size + increment, time_step):
        ax = data[COLUMN_NAMES[1]].values[i: i + segment_time_size]
        ay = data[COLUMN_NAMES[2]].values[i: i + segment_time_size]
        az = data[COLUMN_NAMES[3]].values[i: i + segment_time_size]


        gx = data[COLUMN_NAMES[4]].values[i: i + segment_time_size]
        gy = data[COLUMN_NAMES[5]].values[i: i + segment_time_size]
        gz = data[COLUMN_NAMES[6]].values[i: i + segment_time_size]

        mx = data[COLUMN_NAMES[7]].values[i: i + segment_time_size]
        my = data[COLUMN_NAMES[8]].values[i: i + segment_time_size]
        mz = data[COLUMN_NAMES[9]].values[i: i + segment_time_size]

        # When 9 features used
        data_convoluted.append([ax, ay, az, gx, gy, gz, mx, my, mz])

        # When 3 features used
        # data_convoluted.append([ax, ay, az])

        # Label for a data window is the label that appears most commonly
        label = stats.mode(data[COLUMN_NAMES[0]][i: i + segment_time_size])[0][0]
        labels.append(label)

    data_convoluted = np.asarray(data_convoluted, dtype=np.float32)
    data_convoluted = data_convoluted.transpose(0, 2, 1)

    labels = one_hot_encode(labels)
    return data_convoluted, labels

def one_hot_encode(labels):
    """
    Take as input a list of labels (strings) and encode them using one_hot_encoding scheme,
    i.e. assuming there are 3 activities: A, B in the LABELS_NAMES array,
    if the input is [A, B] then return [[1, 0, 0].[0, 1, 0]].
    If the label does not exist then raise a NameError.
    """
    encoded = []
    for i, label in enumerate(labels):
        array = np.zeros(N_CLASSES)
        try:
            label_position(label)
        except NameError:
            raise NameError
        array[label_position(label)] = 1
        encoded.append(array)

    return np.asarray(encoded, dtype=np.float32)

def label_position(label):
    """
    Take as input a label (string) and if it's in LABELS_NAMES array,
    return its position, otherwise raise NameError.
    """
    for i in range(N_CLASSES):
        if(LABELS_NAMES[i] == label):
            return i
    raise NameError('Label does not exist')

def one_hot_to_label(array):
    """
    Take as input a one-hot encoded array and return a label corresponding to "one".
    i.e for [0, 0, 1] return label at index 2.
    """
    i = np.argmax(array)
    return LABELS_NAMES[i]

def softmax_to_one_hot(array):
    """
    Take an array of numbers as input and return one-hot encoded version of the
    array, where "one" corresponds to the highest number in the array.
    i.e. for [0, 2, 5, 3] return [0, 0, 1, 0]
    """
    i = np.argmax(array)
    one_hot = np.zeros(len(array))
    one_hot[i] = 1
    return one_hot
