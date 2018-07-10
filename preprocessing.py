import numpy as np
import pandas as pd

from scipy import stats

from config import * # Global variables

def get_convoluted_data(data):
    """
    Take as input pandas dataframe and return a tuple: convoluted data and labels.
    Convoluted data is basically the data extracted by sliding a window of size
    SEGMENT_TIME_SIZE with stepsize TIME_STEP. Each window is assigned with one
    label, which is the most frequently occuring label for in given window.
    """
    data_convoluted = []
    labels = []

    increment = 0
    if(len(data) == SEGMENT_TIME_SIZE):
        increment = 1
    elif(len(data) < SEGMENT_TIME_SIZE):
        raise ValueError

    # Slide a "SEGMENT_TIME_SIZE" wide window with a step size of "TIME_STEP"
    #   Increment allows the loop to run if there is just one sample, for which
    #   len(data) == SEGMENT_TIME_SIZE
    for i in range(0, len(data) - SEGMENT_TIME_SIZE + increment, TIME_STEP):
        ax = data[COLUMN_NAMES[1]].values[i: i + SEGMENT_TIME_SIZE]
        ay = data[COLUMN_NAMES[2]].values[i: i + SEGMENT_TIME_SIZE]
        az = data[COLUMN_NAMES[3]].values[i: i + SEGMENT_TIME_SIZE]

        """
        gx = data[COLUMN_NAMES[4]].values[i: i + SEGMENT_TIME_SIZE]
        gy = data[COLUMN_NAMES[5]].values[i: i + SEGMENT_TIME_SIZE]
        gz = data[COLUMN_NAMES[6]].values[i: i + SEGMENT_TIME_SIZE]

        mx = data[COLUMN_NAMES[7]].values[i: i + SEGMENT_TIME_SIZE]
        my = data[COLUMN_NAMES[8]].values[i: i + SEGMENT_TIME_SIZE]
        mz = data[COLUMN_NAMES[9]].values[i: i + SEGMENT_TIME_SIZE]
        """

        data_convoluted.append([ax, ay, az])

        # Label for a data window is the label that appears most commonly
        label = stats.mode(data[COLUMN_NAMES[0]][i: i + SEGMENT_TIME_SIZE])[0][0]
        labels.append(label)

    data_convoluted = np.asarray(data_convoluted, dtype=np.float32)
    data_convoluted = data_convoluted.transpose(0, 2, 1)

    # One-hot encoding
    # Previously used get_dummies
    # labels_ = np.asarray(pd.get_dummies(labels), dtype=np.float32)

    labels = one_hot_encode(labels)
    return data_convoluted, labels

def one_hot_encode(labels):
    """
    Take as input a list of labels (strings) and encode them using one_hot_encoding scheme,
    i.e. assuming there are 3 activities: A, B in the LABELS_NAMES array,
    if the input is [A, B] then return [[1, 0, 0].[0, 1, 0]].
    If the label does not exist then print informative message and exit.
    """
    encoded = []
    for i, label in enumerate(labels):
        array = np.zeros(N_CLASSES)
        try:
            label_position(label)
        except NameError:
            pass
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
