import sys
import numpy as np
import pandas as pd

from config import *

def change_label(data, label):
    for i in data.index:
        data.at[i, COLUMN_NAMES[0]] = label
    print(data)
    return data

if __name__ == '__main__':
    if(len(sys.argv) != 3):
        print("Usage: script [FILENAME] [LABEL]")
        exit()
    file_name = sys.argv[1]
    label = sys.argv[2]

    data = pd.read_pickle(DATA_TEMP_DIR + file_name)
    data_changed = change_label(data, label)
    data_changed.to_pickle(DATA_TEMP_DIR + 'sample_changed.pckl')
