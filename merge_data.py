import pandas as pd
import glob

from config import * # Global variables

def merge_pckls(directory):
    dfs = []
    for file in glob.glob(directory + '*.pckl'):
        data = pd.read_pickle(file)
        dfs.append(data)

    try:
        df = pd.concat(dfs, ignore_index=True)
        df.to_pickle(DATA_TEMP_DIR + 'data_merged.pckl')
        return df
    except ValueError:
        raise ValueError

if __name__ == '__main__':
    try:
        df = merge_pckls(DATA_TEMP_DIR)
        print("Final data shape: ", df.shape)
    except ValueError:
        raise ValueError
